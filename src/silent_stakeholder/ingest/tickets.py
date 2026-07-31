"""Ingest support tickets from `Tobi-Bueck/customer-support-tickets` (HF).

This is a generic, multi-language support corpus — NOT WordPress-specific. We use it
honestly as *cross-source corroboration by need-category*: keep English tickets whose
text echoes the product's job categories (auth/login, media/upload, editor/content,
sync/publish). They enter the pipeline as source="ticket" and only surface as evidence
where they semantically cluster with a real product theme — raising source diversity
without pretending they are the same product.
"""

from __future__ import annotations

import pandas as pd
import requests

from ..config import RAW_DIR
from ..ids import ticket_id
from ..schemas import Signal

PARQUET_URL = (
    "https://huggingface.co/api/datasets/Tobi-Bueck/customer-support-tickets"
    "/parquet/default/train/0.parquet"
)
_CACHE = RAW_DIR / "support_tickets.parquet"

# specific job-category phrases shared with the product's user needs (kept tight to
# avoid generic tickets inflating diversity — anchoring in gap.py is a second guard)
_RELEVANT = (
    "log in", "login", "sign in", "signin", "log-in", "password reset", "authenticat",
    "upload", "media library", "image upload", "attach file", "editor", "publish",
    "draft", "sync", "wordpress", "blog", "website", "cms",
)


def fetch_parquet(force: bool = False) -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if force or not _CACHE.exists():
        with requests.get(PARQUET_URL, timeout=120, stream=True) as r:
            r.raise_for_status()
            with open(_CACHE, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    f.write(chunk)
    return pd.read_parquet(_CACHE)


def load_tickets(*, limit: int = 800) -> list[Signal]:
    if limit <= 0:
        return []
    try:
        df = fetch_parquet()
    except Exception:  # noqa: BLE001 - tickets are an optional cross-source enrichment
        return []
    if "language" in df.columns:
        df = df[df["language"].astype(str).str.lower() == "en"]

    signals: list[Signal] = []
    for idx, row in df.iterrows():
        subject = str(row.get("subject", "")).strip()
        body = str(row.get("body", "")).strip()
        text = f"{subject}. {body}".strip(". ").strip()
        if not text:
            continue
        if not any(k in text.lower() for k in _RELEVANT):
            continue
        signals.append(
            Signal(id=ticket_id(int(idx), text), source="ticket", text=text[:1200])
        )
        if len(signals) >= limit:
            break
    return signals
