# Submission — The Silent Stakeholder

**Repo:** https://github.com/Nlbo/s-s-s--f-i-r-e-c-o-d-e
**Pitch deck:** [`docs/pitch-deck.html`](docs/pitch-deck.html) (animated, Ant-Design; arrow keys to navigate) · [`docs/Silent_Stakeholder_Pitch.pptx`](docs/Silent_Stakeholder_Pitch.pptx) (PowerPoint fallback for Drive)
**Dashboard:** [`docs/sample/report.html`](docs/sample/report.html) (Ant-Design, interactive evidence explorer)
**Product analysed:** WordPress for Android (`org.wordpress.android`)
**Data:** `sealuzh/app_reviews` (2 287 reviews ≤ T0) + `wordpress-mobile/WordPress-Android` GitHub roadmap & issues + `Tobi-Bueck/customer-support-tickets`. T0 = 2017-01-01 (reviews are ~2016; roadmap reconstructed as of T0).

---

## ① One-sentence gap statement
> **Users just want to create an account/blog without mysterious errors — told clearly what went wrong and how to fix it, not left stuck on a silent, generic failure. The 2016 roadmap ignored it — and it's still unfixed today.**

## ② Ranked gaps (full trace in [`docs/sample/report.md`](docs/sample/report.md) · dashboard: [`docs/sample/report.html`](docs/sample/report.html))

| # | Need (user's terms) | Verdict | Conf. | Backtest (proof) |
|---|---|---|---|---|
| 1 | Clear, actionable **errors when creating an account**/blog | IGNORED | 63% | **still unfixed** (no genuine post-T0 fix) |
| 2 | **Video attachment** in posts works reliably | IGNORED | 63% | team shipped **GH-6654**, +8 months |
| 3 | Posts reliably **load & refresh** after login | IGNORED | 62% | team shipped **GH-5874**, +10 months |
| 4 | Reply / like / **comment on comments** in-app | UNDER-PRIORITIZED | 57% | team shipped **GH-6769**, +9 months |
| 5 | **Self-hosted & account login** that "just works" | UNDER-PRIORITIZED | 57% | team shipped **GH-5843**, +10 months |

Every gap carries the four required fields — the need, a **calibrated** confidence with its V/D/I/K/G/X breakdown, an evidence trace by signal ID, and the verdict — in `docs/sample/report.json`. *(Run: gpt-5.1; confidence is logistic-calibrated on 15 backtested gaps, 11 corroborated.)*

**Headline rigor claim:** using **only 2016 signals + the 2016 roadmap**, we surfaced 5 latent needs the roadmap missed. The backtest proves it: the team **shipped 4 of the 5 within 8–10 months**, and the #1 (account-creation errors) they **never genuinely fixed** — exactly the silent stakeholder.

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
- **Backtest** matches each need to the nearest post-T0 issue (Search API, full 2017–2026 coverage) at ≥0.50 similarity, and the report **names the matched issue** so a judge verifies by reading, not by trusting a number.
- **Calibration** is applied only because this run produced label variety (IGNORED + shipped-later) → a logistic fit on N=15 (11 corroborated). With a single-outcome set we report "uncalibrated" instead of faking a curve.
- **No IGNORED-vs-UNDER is forced** — WordPress is well-maintained, so most gaps are eventually addressed (that's *under-prioritized*); the one need never genuinely fixed is ranked #1.
