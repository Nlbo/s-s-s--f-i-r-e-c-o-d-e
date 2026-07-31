"""Calibration must be honest: only claim it with enough backtest labels (SPEC §6/§7)."""

from __future__ import annotations

from silent_stakeholder.agents.calibrate import calibrate
from silent_stakeholder.schemas import ConfidenceBreakdown, Gap, Validation


def _gap(raw: float, verdict: str, built_later: bool | None) -> Gap:
    return Gap(
        rank=0, need="n", confidence=raw,
        confidence_breakdown=ConfidenceBreakdown(V=0, D=0, I=0, K=0, G=0, X=0, raw=raw),
        verdict=verdict, verdict_rationale="", latent_reasoning="",
        validation=Validation(built_later=built_later),
    )


def test_too_few_labels_stays_uncalibrated():
    status, applied = calibrate([_gap(0.5, "IGNORED", None)])
    assert not applied
    assert "uncalibrated" in status


def test_calibration_applies_and_is_monotonic():
    # 12 labels, both classes: high-raw = corroborated, low-raw = not
    gaps = [_gap(0.8, "IGNORED", False) for _ in range(6)]  # IGNORED + not built = correct
    gaps += [_gap(0.2, "IGNORED", True) for _ in range(6)]  # IGNORED + built = wrong
    status, applied = calibrate(gaps)
    assert applied
    assert "N=12" in status
    hi = next(g for g in gaps if g.confidence_breakdown.raw == 0.8)
    lo = next(g for g in gaps if g.confidence_breakdown.raw == 0.2)
    assert hi.confidence > lo.confidence  # higher raw -> higher calibrated P(correct)
