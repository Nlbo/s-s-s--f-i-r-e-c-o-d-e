"""LLM access with a deterministic local fallback (SPEC.md §3, §10).

Two backends behind one interface:
  * OpenAI  — high-quality JTBD extraction (JSON) + embeddings, when OPENAI_API_KEY is set.
  * Fallback — rule-free TF-IDF embeddings (sklearn) + a no-op chat that returns {}.
    Lets the whole pipeline run offline and makes tests network-free and reproducible.

All LLM calls are cached by content hash under .llm_cache so runs are cheap and
deterministic, and untrusted model output is always parsed as JSON (never executed).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import LLM_CACHE_DIR, Settings


class LLMClient:
    def __init__(self, settings: Settings, *, offline: bool = False) -> None:
        self.settings = settings
        backend = "offline" if offline else settings.backend
        self.backend = backend
        self.offline = backend == "offline"          # gates chat (extract/verdict/critic)
        self._embed_openai = backend == "openai" and bool(settings.openai_embed_model)
        self._client = None
        self._chat_model = ""
        LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        if backend != "offline":
            from openai import OpenAI

            if backend == "router":
                base = settings.llm_url.rstrip("/") + "/v1"
                self._client = OpenAI(api_key=settings.llm_key, base_url=base)
                self._chat_model = settings.llm_model
            else:
                self._client = OpenAI(api_key=settings.openai_api_key)
                self._chat_model = settings.openai_model

    # ---- cache -------------------------------------------------------------
    def _cache_path(self, kind: str, key: str) -> Path:
        h = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        return LLM_CACHE_DIR / f"{kind}_{h}.json"

    # ---- chat (structured JSON) -------------------------------------------
    @retry(stop=stop_after_attempt(4), wait=wait_exponential(min=1, max=20))
    def _chat_raw(self, system: str, user: str) -> str:
        assert self._client is not None
        resp = self._client.chat.completions.create(
            model=self._chat_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return resp.choices[0].message.content or "{}"

    def chat_json(self, system: str, user: str) -> dict:
        """Return a parsed JSON object. Offline -> {} (callers must handle)."""
        if self.offline:
            return {}
        # model is part of the cache key so switching models yields fresh (not reused) results
        cp = self._cache_path("chat", self._chat_model + "\x1f" + system + "\x1f" + user)
        if cp.exists():
            return json.loads(cp.read_text())
        try:
            data = json.loads(self._chat_raw(system, user))
        except Exception:  # noqa: BLE001 - any LLM/API failure falls back to the heuristic
            return {}  # transient failure: do NOT cache, so a later run can retry
        if not isinstance(data, dict):
            data = {}
        cp.write_text(json.dumps(data))  # cache only successful parses
        return data

    # ---- embeddings --------------------------------------------------------
    @retry(stop=stop_after_attempt(4), wait=wait_exponential(min=1, max=20))
    def _embed_openai_call(self, texts: list[str]) -> np.ndarray:
        assert self._client is not None
        vecs: list[list[float]] = []
        for i in range(0, len(texts), 256):
            batch = [t[:8000] for t in texts[i : i + 256]]
            resp = self._client.embeddings.create(
                model=self.settings.openai_embed_model, input=batch
            )
            vecs.extend(d.embedding for d in resp.data)
        return np.asarray(vecs, dtype=np.float32)

    def embed(self, texts: list[str]) -> np.ndarray:
        """Return L2-normalized embeddings for `texts`.

        Offline: TF-IDF -> TruncatedSVD (transductive over the given corpus).
        The whole corpus for a stage should be embedded in one call so vectors
        share a space (needed for signal<->roadmap similarity).
        """
        if not texts:
            return np.zeros((0, 1), dtype=np.float32)
        vecs = self._embed_openai_call(texts) if self._embed_openai else self._embed_tfidf(texts)
        # Deterministically de-zero empty rows (e.g. reviews that are all stop-words):
        # give each a distinct basis spike so cosine is defined and they scatter into
        # tiny clusters that min_size filters out — instead of collapsing to the origin.
        d = vecs.shape[1]
        zero_rows = np.where(~vecs.any(axis=1))[0]
        for r in zero_rows:
            vecs[r, int(r) % d] = 1.0
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vecs / norms

    @staticmethod
    def _embed_tfidf(texts: list[str]) -> np.ndarray:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer

        tfidf = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2), min_df=2, max_features=20000
        )
        X = tfidf.fit_transform(texts)
        n_comp = int(min(256, max(2, min(X.shape) - 1)))
        if X.shape[1] <= n_comp or X.shape[0] <= 2:
            return X.toarray().astype(np.float32)
        return TruncatedSVD(n_components=n_comp, random_state=0).fit_transform(X).astype(np.float32)
