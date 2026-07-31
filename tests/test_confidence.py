"""Confidence model must be well-behaved and defensible (SPEC §6)."""

from __future__ import annotations

from silent_stakeholder.config import ConfidenceWeights


def test_score_is_bounded():
    w = ConfidenceWeights()
    hi = w.score(volume=1, diversity=1, intensity=1, cohesion=1, gap_clarity=1, contradiction=0)
    lo = w.score(volume=0, diversity=0, intensity=0, cohesion=0, gap_clarity=0, contradiction=1)
    assert 0.05 <= lo <= hi <= 0.95


def test_gap_clarity_increases_confidence():
    w = ConfidenceWeights()
    base = dict(volume=0.5, diversity=0.5, intensity=0.5, cohesion=0.5, contradiction=0.1)
    assert w.score(gap_clarity=0.9, **base) > w.score(gap_clarity=0.2, **base)


def test_contradiction_penalizes():
    w = ConfidenceWeights()
    base = dict(volume=0.6, diversity=0.6, intensity=0.6, cohesion=0.6, gap_clarity=0.7)
    assert w.score(contradiction=0.0, **base) > w.score(contradiction=0.8, **base)


def test_gap_clarity_is_dominant_weight():
    w = ConfidenceWeights()
    assert w.gap_clarity == max(
        w.volume, w.diversity, w.intensity, w.cohesion, w.gap_clarity
    )
