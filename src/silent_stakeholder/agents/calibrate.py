"""Confidence calibration (SPEC.md §6/§7).

The transparent score (`raw`) is turned into an empirically meaningful probability by
fitting a 1-D logistic map raw -> P(gap was genuinely under-served) over the candidate
gaps with a backtest label. The label is **discriminating, not auto-pass**:

  * never delivered (no post-T0 match, or still open)        -> corroborated (real gap)
  * delivered, but only after a long lag (>= LAG_MONTHS)      -> corroborated (under-served)
  * delivered quickly (< LAG_MONTHS after T0)                 -> NOT corroborated
        (the team was already on it — our "gap" was weak)

So a gap the team fixed in two months is scored as a miss, and one they took ten months
on — or never did — as a hit. That gives real class variety instead of rubber-stamping
every verdict. Too few labels or a single outcome -> we stay honestly "uncalibrated".
"""

from __future__ import annotations

import numpy as np

from ..schemas import Gap

MIN_LABELS = 8
LAG_MONTHS = 6  # a fix shipped faster than this doesn't confirm an under-served gap


def corroborated(g: Gap) -> bool | None:
    """True if hindsight confirms a genuine, under-served gap; False if the team handled
    it promptly; None if there is no backtest label. Verdict-independent by design."""
    v = g.validation
    if v.built_later is None:
        return None
    if v.built_later is False:
        return True  # never delivered -> a real, still-unmet need
    return (v.lag_months or 0) >= LAG_MONTHS  # delivered: only a hit if they were slow


def calibrate(gaps: list[Gap]) -> tuple[str, bool]:
    """Fit + apply calibration in place. Returns (status_message, applied)."""
    labels = [(g.confidence_breakdown.raw, corroborated(g)) for g in gaps]
    labeled = [(x, int(y)) for x, y in labels if y is not None]
    n = len(labeled)
    classes = {y for _, y in labeled}
    if n < MIN_LABELS:
        return (f"uncalibrated: only {n} backtest labels (need >= {MIN_LABELS})", False)
    if len(classes) < 2:
        return (f"uncalibrated: all {n} backtest labels one outcome (no contrast)", False)
    correct = sum(c for _, c in labeled)
    minority = min(correct, n - correct)
    if minority < 3:
        # 14/15 "genuine" is great validation but too little negative contrast to fit a
        # meaningful curve — calibrating anyway collapses every gap to one number. Keep the
        # transparent (varying) score, which still differentiates gaps as the rubric wants.
        return (
            f"uncalibrated: backtest labels too skewed ({correct}/{n} corroborated) — "
            "transparent score kept",
            False,
        )

    from sklearn.linear_model import LogisticRegression

    x = np.array([[r] for r, _ in labeled], dtype=float)
    y = np.array([c for _, c in labeled], dtype=int)
    model = LogisticRegression().fit(x, y)
    for g in gaps:
        p = float(model.predict_proba([[g.confidence_breakdown.raw]])[0, 1])
        g.confidence = round(max(0.05, min(0.95, p)), 3)
    return (f"logistic calibration on N={n} backtested gaps ({correct} corroborated)", True)
