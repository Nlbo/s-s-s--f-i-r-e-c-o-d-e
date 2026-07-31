"""CriticAgent (SPEC.md §4[5]): adversarially try to *falsify* each gap. Gaps that
survive the null hypothesis rank higher; the critique is stored as ammunition for the
live defense ("here's a gap you missed / isn't this just a frequent complaint?").
"""

from __future__ import annotations

import json

from tqdm import tqdm

from ..llm import LLMClient
from ..schemas import Gap, Signal
from .gap import GapCandidate

LATENCY_FLOOR = 0.30    # below this, the "need" reads as a surface complaint
COVERAGE_CEIL = 0.65    # above this, the roadmap may already address it


def _heuristic(gap: Gap, cand: GapCandidate) -> tuple[str, bool, float]:
    objections: list[str] = []
    if cand.theme.latency < LATENCY_FLOOR:
        objections.append(
            f"low latency ({cand.theme.latency:.2f}): users mostly state this explicitly, "
            "so it's closer to a surface complaint than a hidden need"
        )
    # A highly-similar roadmap item only *falsifies* an IGNORED claim. For
    # UNDER-PRIORITIZED / MISUNDERSTOOD a related item is expected by definition —
    # penalising them for it contradicts the verdict, so it is not an objection there.
    if gap.verdict == "IGNORED" and cand.max_sim > COVERAGE_CEIL:
        objections.append(
            f"claimed IGNORED, but a roadmap item is {cand.max_sim:.2f} similar — "
            "it may already be covered"
        )
    if gap.confidence_breakdown.X > 0.4:
        objections.append(
            f"mixed signals (X={gap.confidence_breakdown.X:.2f}): a notable share of members "
            "are non-pain/satisfied, so the theme isn't unanimous"
        )
    if gap.confidence_breakdown.D < 0.34:
        objections.append("single-source evidence — not yet corroborated across sources")

    fatal = [o for o in objections if "surface complaint" in o or "already be covered" in o]
    survives = len(fatal) == 0
    _held = {
        "IGNORED": "no near roadmap item addresses it",
        "UNDER-PRIORITIZED": "the related roadmap item is under-prioritized vs the signal",
        "MISUNDERSTOOD": "the roadmap frames it differently than users experience it",
    }[gap.verdict]
    if not objections:
        text = (
            f"Survived falsification: high latency, {_held}, and evidence is "
            "intensity-weighted rather than cherry-picked."
        )
        return text, True, 1.0
    penalty = 0.90 ** len(objections)
    verdict_word = "Survived with caveats" if survives else "Weak — likely not a top gap"
    text = f"{verdict_word}. Objections considered: " + "; ".join(objections) + "."
    return text, survives, penalty


_SYS = (
    "You are a skeptical judge trying to DISPROVE a claimed product gap. Argue the null "
    "hypothesis: is it just a frequent complaint (not latent)? Is it already on the roadmap? "
    "Is the evidence sarcastic/cherry-picked/contradictory? Decide if the gap survives. "
    'Return JSON: {"survives":bool,"confidence_multiplier":0.5..1.0,"critique":str}'
)


def critique(
    llm: LLMClient, gap: Gap, cand: GapCandidate, signals_by_id: dict[str, Signal]
) -> tuple[str, bool, float]:
    if llm.offline:
        return _heuristic(gap, cand)
    quotes = [
        {"id": e.id, "star": e.star, "quote": e.quote} for e in gap.evidence_signals[:6]
    ]
    payload = {
        "need": gap.need,
        "verdict": gap.verdict,
        "latency": cand.theme.latency,
        "max_roadmap_similarity": cand.max_sim,
        "confidence_features": gap.confidence_breakdown.model_dump(),
        "evidence": quotes,
    }
    data = llm.chat_json(_SYS, json.dumps(payload, ensure_ascii=False))
    if not data:
        return _heuristic(gap, cand)
    survives = bool(data.get("survives", True))
    mult = max(0.5, min(1.0, float(data.get("confidence_multiplier", 1.0))))
    text = str(data.get("critique", ""))[:600] or _heuristic(gap, cand)[0]
    return text, survives, mult


def critique_all(
    llm: LLMClient, gaps: list[Gap], cands: list[GapCandidate], signals: list[Signal]
) -> tuple[list[Gap], list[bool]]:
    """Annotate each gap with its critique + adjusted confidence; return (gaps, survives)."""
    by_id = {s.id: s for s in signals}
    survives_flags: list[bool] = []
    for gap, cand in tqdm(
        list(zip(gaps, cands, strict=True)), desc="  critic", unit="gap"
    ):
        # The critic is a survival gate + a stored rebuttal — it does NOT rescale the
        # confidence, which must stay the calibrated probability (SPEC §6).
        text, survives, _mult = critique(llm, gap, cand, by_id)
        gap.adversarial_check = text
        survives_flags.append(survives)
    return gaps, survives_flags
