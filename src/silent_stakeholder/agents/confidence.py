"""ConfidenceAgent (SPEC.md §6): turn a GapCandidate into a scored Gap using a
transparent linear model over measured features — so "defend this score" is answered
by pointing at the feature vector, not a black box.
"""

from __future__ import annotations

import math

from ..config import Settings
from ..schemas import ConfidenceBreakdown, EvidenceSignal, Gap, Signal
from .gap import GapCandidate

V_SAT = 60          # signal count at which volume feature saturates to ~1
REACT_SAT = 20      # github reactions at which demand intensity saturates


def _signal_intensity(s: Signal) -> float:
    if s.source == "review" and s.star is not None:
        return max(0.0, min(1.0, (3 - s.star) / 2))     # 1★->1, 2★->0.5, 3★->0
    if s.source == "gh_issue":
        return min(1.0, s.reactions / REACT_SAT)
    return 0.5                                            # ticket: unknown -> neutral


def _pick_evidence(members: list[Signal], k: int = 6) -> list[EvidenceSignal]:
    # strongest first (lowest star / highest reactions), then ensure source variety
    ranked = sorted(members, key=_signal_intensity, reverse=True)
    chosen: list[Signal] = []
    seen_sources: set[str] = set()
    for s in ranked:
        if len(chosen) >= k:
            break
        chosen.append(s)
        seen_sources.add(s.source)
    # try to include at least one of each present source
    for s in ranked:
        if len(chosen) >= k:
            break
        if s.source not in seen_sources:
            chosen.append(s)
            seen_sources.add(s.source)
    return [
        EvidenceSignal(
            id=s.id, source=s.source, star=s.star, reactions=s.reactions,
            date=s.date, quote=s.text[:240],
        )
        for s in chosen
    ]


def score_gap(settings: Settings, cand: GapCandidate, signals_by_id: dict[str, Signal]) -> Gap:
    members = [signals_by_id[sid] for sid in cand.theme.signal_ids if sid in signals_by_id]
    n = len(members) or 1

    # Single-letter names mirror the SPEC §6 confidence-formula notation.
    V = min(1.0, math.log1p(n) / math.log1p(V_SAT))
    D = len({s.source for s in members}) / 3
    I = sum(_signal_intensity(s) for s in members) / n  # noqa: E741 - SPEC notation
    K = cand.theme.cohesion
    G = cand.gap_clarity
    X = sum(1 for s in members if s.star is not None and s.star >= 4) / n  # internal disagreement

    raw = (
        settings.weights.volume * V
        + settings.weights.diversity * D
        + settings.weights.intensity * I
        + settings.weights.cohesion * K
        + settings.weights.gap_clarity * G
        - settings.weights.contradiction_penalty * X
    )
    confidence = max(0.05, min(0.95, raw))

    return Gap(
        rank=0,
        need=cand.need_restated,
        confidence=round(confidence, 3),
        confidence_breakdown=ConfidenceBreakdown(
            V=round(V, 3), D=round(D, 3), I=round(I, 3), K=round(K, 3),
            G=round(G, 3), X=round(X, 3), raw=round(raw, 3),
        ),
        verdict=cand.verdict,
        verdict_rationale=cand.rationale,
        latent_reasoning=cand.latent_reasoning,
        evidence_signals=_pick_evidence(members),
        roadmap_refs=cand.roadmap_refs,
        theme_id=cand.theme.id,
    )


def score_all(
    settings: Settings, candidates: list[GapCandidate], signals: list[Signal]
) -> list[Gap]:
    by_id = {s.id: s for s in signals}
    return [score_gap(settings, c, by_id) for c in candidates]
