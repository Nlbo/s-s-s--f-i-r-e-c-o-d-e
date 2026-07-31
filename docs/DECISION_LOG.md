# Decision Log

Chronological record of key decisions and *which agent* made each — for honest,
defensible provenance (and live-defense prep). Newest at the bottom.

| # | Decision | Rationale | By |
|---|----------|-----------|----|
| 1 | Product = WordPress for Android (`org.wordpress.android`) | Only candidate with **both** dataset reviews (avg ★3.29 → rich pain signal) **and** a deep, label-structured GitHub roadmap (100+ milestones, `[Pri]`/`[Type]` labels). Verified against the parquet + GitHub API, not guessed. | orchestrator |
| 2 | Historical backtest design (T0 = 2017-01-01) | Reviews are ~2016; full repo history to 2026 lets us validate predictions against what was actually built → empirical rigor instead of assertion. | orchestrator |
| 3 | Signals = reviews + user-filed GH issues (+ reactions) + relevant tickets; Roadmap = milestones + prioritized/labeled issues | Gives two sides of one product with a principled, traceable split. | orchestrator |
| 4 | Deterministic local fallback (TF-IDF + rules) alongside OpenAI | Pipeline must run and be testable without a key; keeps CI offline and reproducible. | orchestrator |
| 5 | Confidence = transparent linear model over measured features (not LLM vibe) | Must be defensible on the spot ("defend this score") and calibratable against backtest. | orchestrator |
| 6 | Bypass Adobe Artifactory; install from public PyPI | Artifactory index unreachable in this env and embeds a plaintext token; public PyPI reachable and avoids touching the credential. | orchestrator |
| 7 | Ran an adversarial code+rigor review agent over the whole codebase | The user wants "agent implemented → agent reviewed → agent checked". A dedicated reviewer read SPEC + all src, ran ruff/pytest/pipeline, and found 10 real issues (see below). | reviewer agent |
| 8 | Fixed all review findings before the real run | Reviewer found the two headline claims were broken: backtest **crashed** with a token (unbounded paging → 422) and was vacuous without one; "calibrated" had no calibration code; X-feature was review-only; fallback need was keyword-salad; critic text contradicted its verdict. Fixed each; added real logistic calibration + concurrency. | orchestrator |
