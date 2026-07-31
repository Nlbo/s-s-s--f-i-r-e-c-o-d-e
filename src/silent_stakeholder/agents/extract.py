"""ExtractorAgent (SPEC.md §4[1]): Signal -> NeedUnit via Jobs-To-Be-Done framing.

Latency is born here: we separate the *job* the user is trying to get done and the
*obstacle* from what they *literally asked for* (expressed_solution). A signal with a
strong obstacle but no expressed_solution is latent-leaning.

LLM path batches signals to keep cost low; fallback is deterministic rules + lexicons.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..llm import LLMClient
from ..schemas import NeedUnit, Signal

# --- lexicons for the deterministic fallback -------------------------------
CHURN = [
    "uninstall", "uninstalled", "deleting", "deleted the app", "switch to", "switching",
    "used to", "no longer", "gave up", "waste of", "stopped using", "moving to",
    "lost my", "lost all", "won't use", "one star", "worst", "useless",
]
ASK = [
    "please add", "would be nice", "would like", "i wish", "wish it", "need a", "needs a",
    "should have", "should be able", "option to", "allow ", "ability to", "feature request",
    "make it possible", "please make", "please fix", "add a", "add an", "bring back",
]
WORKAROUND = [
    "instead i", "i have to", "have to manually", "workaround", "manually", "every time i",
    "export to", "copy and paste", "copy paste", "log in again", "reinstall",
]
_STAR_SENT = {1: -1.0, 2: -0.5, 3: 0.0, 4: 0.5, 5: 1.0}
_SENT_NEG = ["crash", "bug", "broken", "fail", "error", "slow", "can't", "cannot", "won't",
             "doesn't", "annoying", "terrible", "hate", "frustrat", "problem", "issue", "worse"]


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _first_hits(text: str, phrases: list[str]) -> list[str]:
    low = text.lower()
    return [p.strip() for p in phrases if p in low]


def _rule_extract(sig: Signal) -> NeedUnit:
    text = _clean(sig.text)
    low = text.lower()
    if sig.star is not None:
        sentiment = _STAR_SENT.get(sig.star, 0.0)
    else:
        neg = sum(low.count(w) for w in _SENT_NEG)
        sentiment = max(-1.0, -0.25 * neg)
    asks = _first_hits(text, ASK)
    return NeedUnit(
        signal_id=sig.id,
        job=text[:220],
        obstacle=text[:220] if sentiment < 0 else "",
        expressed_solution=asks[0] if asks else None,
        is_workaround=bool(_first_hits(text, WORKAROUND)),
        sentiment=sentiment,
        churn_markers=_first_hits(text, CHURN),
    )


_SYS = (
    "You are a product analyst extracting latent user needs from noisy feedback. "
    "For each item return the underlying Job-To-Be-Done, the obstacle, and — separately — "
    "whether the user explicitly named a solution/feature (expressed_solution) or only "
    "described a pain/workaround. Be terse and faithful; do not invent needs. "
    'Return JSON: {"items":[{"i":int,"job":str,"obstacle":str,'
    '"expressed_solution":str|null,"is_workaround":bool,"sentiment":number in [-1,1],'
    '"churn_markers":[str]}]}'
)


def _llm_extract_batch(llm: LLMClient, sigs: list[Signal]) -> list[NeedUnit]:
    payload = [{"i": i, "star": s.star, "text": s.text[:900]} for i, s in enumerate(sigs)]
    data = llm.chat_json(_SYS, json.dumps(payload, ensure_ascii=False))
    by_i: dict[int, dict] = {}
    for it in data.get("items", []) if isinstance(data, dict) else []:
        if isinstance(it, dict) and isinstance(it.get("i"), int):
            by_i[it["i"]] = it
    out: list[NeedUnit] = []
    for i, sig in enumerate(sigs):
        it = by_i.get(i)
        if not it:
            out.append(_rule_extract(sig))
            continue
        try:
            out.append(
                NeedUnit(
                    signal_id=sig.id,
                    job=str(it.get("job", ""))[:300] or _clean(sig.text)[:220],
                    obstacle=str(it.get("obstacle", ""))[:300],
                    expressed_solution=(it.get("expressed_solution") or None),
                    is_workaround=bool(it.get("is_workaround", False)),
                    sentiment=max(-1.0, min(1.0, float(it.get("sentiment", 0.0)))),
                    churn_markers=[str(x) for x in (it.get("churn_markers") or [])][:8],
                )
            )
        except (ValueError, TypeError):
            out.append(_rule_extract(sig))
    return out


def extract_need_units(
    llm: LLMClient, signals: list[Signal], *, batch_size: int = 12
) -> list[NeedUnit]:
    if llm.offline:
        return [_rule_extract(s) for s in signals]

    batches = [signals[i : i + batch_size] for i in range(0, len(signals), batch_size)]
    workers = max(1, llm.settings.llm_max_concurrency)
    results: list[list[NeedUnit]] = [[] for _ in batches]
    with ThreadPoolExecutor(max_workers=workers) as ex:  # cache makes calls idempotent
        futures = {ex.submit(_llm_extract_batch, llm, b): i for i, b in enumerate(batches)}
        for fut in as_completed(futures):
            results[futures[fut]] = fut.result()
    return [u for batch in results for u in batch]
