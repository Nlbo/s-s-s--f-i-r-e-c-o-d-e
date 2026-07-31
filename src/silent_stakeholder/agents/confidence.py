"""ConfidenceAgent (SPEC.md §6): turn a GapCandidate into a scored Gap using the
transparent linear model in ConfidenceWeights.score() — the SAME code path that the
unit tests exercise — so "defend this score" is answered by pointing at the feature
vector, not a black box.
"""

from __future__ import annotations

import math
from collections import Counter

from ..config import Settings
from ..schemas import ConfidenceBreakdown, EvidenceSignal, Gap, Signal
from .gap import GapCandidate

V_SAT = 150         # signal count at which the volume feature saturates to ~1
REACT_SAT = 20      # github reactions at which demand intensity saturates


def _signal_intensity(s: Signal, sentiment: float) -> float:
    """Per-signal pain/demand intensity in [0,1], defined for every source."""
    if s.source == "review" and s.star is not None:
        return max(0.0, min(1.0, (3 - s.star) / 2))     # 1★->1, 2★->0.5, 3★->0
    if s.source == "gh_issue":
        return max(min(1.0, s.reactions / REACT_SAT), max(0.0, -sentiment))
    return max(0.0, -sentiment)                          # ticket: from extracted sentiment


def _pick_evidence(members: list[Signal], k: int, sent: dict[str, float]) -> list[EvidenceSignal]:
    """Strongest evidence first, but guarantee one signal per present source so the
    trace visibly spans reviews / github / tickets (SPEC: reads across both sources)."""
    ranked = sorted(members, key=lambda s: _signal_intensity(s, sent.get(s.id, 0.0)), reverse=True)
    by_source: dict[str, list[Signal]] = {}
    for s in ranked:
        by_source.setdefault(s.source, []).append(s)

    chosen: list[Signal] = [lst[0] for lst in by_source.values()]  # 1 per source
    chosen_ids = {s.id for s in chosen}
    for s in ranked:
        if len(chosen) >= k:
            break
        if s.id not in chosen_ids:
            chosen.append(s)
            chosen_ids.add(s.id)
    chosen = sorted(
        chosen[:k], key=lambda s: _signal_intensity(s, sent.get(s.id, 0.0)), reverse=True
    )
    return [
        EvidenceSignal(
            id=s.id, source=s.source, star=s.star, reactions=s.reactions,
            date=s.date, quote=s.text[:240],
        )
        for s in chosen
    ]


def score_gap(
    settings: Settings,
    cand: GapCandidate,
    signals_by_id: dict[str, Signal],
    sentiment_by_id: dict[str, float],
) -> Gap:
    members = [signals_by_id[sid] for sid in cand.theme.signal_ids if sid in signals_by_id]
    n = len(members) or 1

    volume = min(1.0, math.log1p(n) / math.log1p(V_SAT))
    # A source counts toward diversity only with >= 2 signals, so a single loosely-matched
    # generic ticket can't inflate D (the primary source still always counts).
    src_counts = Counter(s.source for s in members)
    diversity = max(len([s for s, c in src_counts.items() if c >= 2]), 1) / 3
    intensity = sum(_signal_intensity(s, sentiment_by_id.get(s.id, 0.0)) for s in members) / n
    cohesion = cand.theme.cohesion
    gap_clarity = cand.gap_clarity
    # contradiction = share of members that are NOT pain (positive/satisfied), i.e. the
    # theme carries conflicting voices — measured across ALL sources via extracted sentiment.
    contradiction = sum(1 for s in members if sentiment_by_id.get(s.id, 0.0) > 0.2) / n

    confidence = settings.weights.score(
        volume=volume, diversity=diversity, intensity=intensity,
        cohesion=cohesion, gap_clarity=gap_clarity, contradiction=contradiction,
    )
    raw = (
        settings.weights.volume * volume
        + settings.weights.diversity * diversity
        + settings.weights.intensity * intensity
        + settings.weights.cohesion * cohesion
        + settings.weights.gap_clarity * gap_clarity
        - settings.weights.contradiction_penalty * contradiction
    )

    return Gap(
        rank=0,
        need=cand.need_restated,
        confidence=round(confidence, 3),
        confidence_breakdown=ConfidenceBreakdown(
            V=round(volume, 3), D=round(diversity, 3), I=round(intensity, 3),
            K=round(cohesion, 3), G=round(gap_clarity, 3), X=round(contradiction, 3),
            raw=round(raw, 3),
        ),
        verdict=cand.verdict,
        verdict_rationale=cand.rationale,
        latent_reasoning=cand.latent_reasoning,
        evidence_signals=_pick_evidence(members, 6, sentiment_by_id),
        roadmap_refs=cand.roadmap_refs,
        theme_id=cand.theme.id,
    )


def score_all(
    settings: Settings,
    candidates: list[GapCandidate],
    signals: list[Signal],
    sentiment_by_id: dict[str, float] | None = None,
) -> list[Gap]:
    by_id = {s.id: s for s in signals}
    sent = sentiment_by_id or {}
    return [score_gap(settings, c, by_id, sent) for c in candidates]
