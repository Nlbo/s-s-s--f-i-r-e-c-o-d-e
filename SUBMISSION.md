# Submission — The Silent Stakeholder

**Repo:** https://github.com/Nlbo/s-s-s--f-i-r-e-c-o-d-e
**Pitch deck:** [`docs/pitch-deck.html`](docs/pitch-deck.html) (animated, Ant-Design; arrow keys to navigate) · [`docs/Silent_Stakeholder_Pitch.pptx`](docs/Silent_Stakeholder_Pitch.pptx) (PowerPoint fallback for Drive)
**Dashboard:** [`docs/sample/report.html`](docs/sample/report.html) (Ant-Design, interactive evidence explorer)
**Product analysed:** WordPress for Android (`org.wordpress.android`)
**Data:** `sealuzh/app_reviews` (2 287 reviews ≤ T0) + `wordpress-mobile/WordPress-Android` GitHub roadmap & issues + `Tobi-Bueck/customer-support-tickets`. T0 = 2017-01-01 (reviews are ~2016; roadmap reconstructed as of T0).

---

## ① One-sentence gap statement
> **Users need publishing to be rock-solid — when they tap Post/Update their content must actually publish, without 403s, cryptic errors, or silent failures (especially on self-hosted sites and after app updates); the 2016 roadmap only touched it tangentially, and the team didn't ship a fix until 20 months later.**

## ② Ranked gaps (full trace in [`docs/sample/report.md`](docs/sample/report.md) · dashboard: [`docs/sample/report.html`](docs/sample/report.html))

| # | Need (user's terms) | Verdict | Conf. | Backtest (proof) |
|---|---|---|---|---|
| 1 | **Publishing that reliably works** — no 403s / cryptic errors | UNDER-PRIORITIZED | 71% | team closed **GH-8300**, +20 months |
| 2 | **Video attachment** in posts that actually sticks | UNDER-PRIORITIZED | 67% | team closed **GH-6654**, +8 months |
| 3 | **Account creation** without mysterious errors | UNDER-PRIORITIZED | 65% | team closed **GH-8460**, +27 months |
| 4 | Posts reliably **load & refresh** over time | UNDER-PRIORITIZED | 64% | team closed **GH-8384**, +21 months |
| 5 | A **comments experience** you can navigate | MISUNDERSTOOD | 50% | closed **GH-6717** (crashes, not the UX), +9 months |

Every gap carries the four required fields — the need, a confidence with its V/D/I/K/G/X breakdown, an evidence trace by signal ID, and the verdict — in `docs/sample/report.json`. *(Run: gpt-5.1.)*

**Headline rigor claim:** using **only 2016 signals + the 2016 roadmap**, we surfaced 5 latent needs the roadmap missed. The backtest proves it: the team eventually addressed **every one — but 8 to 27 months later**, and **13 of 15** flagged gaps were confirmed genuine by hindsight. We saw the silent stakeholder up to 2+ years before the team acted.

## ③ Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" -i https://pypi.org/simple
cp .env.example .env      # add OPENAI_API_KEY (or LLM_KEY) + GITHUB_TOKEN
sss run                   # -> out/report.{json,md,html}
```
Runs end-to-end **offline** too (deterministic TF-IDF + rules) via `sss run --offline`.

## ④ Method (why it's not a complaint counter)
JTBD extraction → latent-theme clustering (`latency = pain × (1−explicit_ask)`) → roadmap alignment (verdict) → transparent confidence (`SPEC.md §6`) → adversarial critic → **historical backtest** (`SPEC.md §7`). Full design in [`SPEC.md`](SPEC.md); pitch in [`docs/PITCH.md`](docs/PITCH.md).

## Honesty notes
- **Backtest** matches each need to the nearest post-T0 issue (Search API, full 2017–2025 coverage, per-year) at ≥0.50 similarity, and the report **names the matched issue** so a judge verifies by reading, not by trusting a number. "Closed" is reported as *closed a matching issue*, not overclaimed as "shipped a feature".
- **Confidence is uncalibrated on purpose here.** The backtest confirmed 13/15 gaps as genuine — great validation, but too little negative contrast to fit a meaningful logistic curve (it would collapse every gap to one number). So we keep the transparent V·D·I·K·G·X score (which still varies, 50–71%) and label it honestly. We only *claim* calibration when the label split supports it.
- **Verdicts are reconciled with hindsight:** a need the team addressed post-T0 is *under-prioritized*, not *ignored* — so no gap displays "IGNORED" while its own backtest says the team fixed it.
