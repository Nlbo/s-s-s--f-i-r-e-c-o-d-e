"""Confidence calibration (SPEC.md §6/§7).

The transparent score (`raw`) is turned into an empirically meaningful probability by
fitting a 1-D logistic map raw -> P(verdict is correct) over the candidate gaps that
have a backtest label. "Correct" = the verdict was corroborated by post-T0 history:
  * IGNORED            -> not built later
  * UNDER-PRIORITIZED  -> shipped late, or still open (never delivered)
  * MISUNDERSTOOD      -> team shipped something later

If there are too few labels (no GITHUB_TOKEN, or a tiny corpus) we do NOT pretend to
calibrate — confidence stays the transparent score and the report says "uncalibrated".
This is deliberately honest: we only claim calibration when we can back it with data.
"""

from __future__ import annotations

import numpy as np

from ..schemas import Gap

MIN_LABELS = 8


def corroborated(g: Gap) -> bool | None:
    v = g.validation
    if v.built_later is None:
        return None
    if g.verdict == "IGNORED":
        return v.built_later is False
    return bool(v.built_later) or bool(v.still_open)


def calibrate(gaps: list[Gap]) -> tuple[str, bool]:
    """Fit + apply calibration in place. Returns (status_message, applied)."""
    labels = [(g.confidence_breakdown.raw, corroborated(g)) for g in gaps]
    labeled = [(x, int(y)) for x, y in labels if y is not None]
    n = len(labeled)
    classes = {y for _, y in labeled}
    if n < MIN_LABELS or len(classes) < 2:
        return (f"uncalibrated (transparent score; only {n} backtest labels)", False)

    from sklearn.linear_model import LogisticRegression

    x = np.array([[r] for r, _ in labeled], dtype=float)
    y = np.array([c for _, c in labeled], dtype=int)
    model = LogisticRegression().fit(x, y)
    for g in gaps:
        p = float(model.predict_proba([[g.confidence_breakdown.raw]])[0, 1])
        g.confidence = round(max(0.05, min(0.95, p)), 3)
    correct = sum(y)
    return (f"logistic calibration on N={n} backtested gaps ({correct} corroborated)", True)
