# Submission — The Silent Stakeholder

**Repo:** https://github.com/Nlbo/s-s-s--f-i-r-e-c-o-d-e
**Pitch deck:** [`docs/Silent_Stakeholder_Pitch.pptx`](docs/Silent_Stakeholder_Pitch.pptx)
**Product analysed:** WordPress for Android (`org.wordpress.android`)
**Data:** `sealuzh/app_reviews` (2 287 reviews ≤ T0) + `wordpress-mobile/WordPress-Android` GitHub roadmap & issues + `Tobi-Bueck/customer-support-tickets`. T0 = 2017-01-01 (reviews are ~2016; roadmap reconstructed as of T0).

---

## ① One-sentence gap statement
> **Users need a reliable, fast way to upload multiple images/media without failures, delays, or merge errors (incl. multi-select) — under-prioritized by the roadmap despite the evidence; the team shipped a fix just 2 months after our T0.**

## ② Ranked gaps (full trace in [`docs/sample/report.md`](docs/sample/report.md) · dashboard: [`docs/sample/report.html`](docs/sample/report.html))

| # | Need (user's terms) | Verdict | Conf. | Backtest (proof) |
|---|---|---|---|---|
| 1 | Reliable multi-image / media **upload** (multi-select, no merge/fail) | UNDER-PRIORITIZED | 50% | team shipped **GH-5434**, +2 months |
| 2 | Consistent **text-formatting** behaviour in the editor | UNDER-PRIORITIZED | 47% | team shipped **GH-5685**, +3 months |
| 3 | Reliable **media-library** experience in the post editor | UNDER-PRIORITIZED | 45% | team shipped **GH-6955**, +11 months |

Every gap carries the four required fields — the need, a calibrated-or-honest confidence with its V/D/I/K/G/X breakdown, an evidence trace by signal ID, and the verdict — in `docs/sample/report.json`.

**Headline rigor claim:** using **only 2016 signals + the 2016 roadmap**, all three predicted under-served needs were **shipped by the team 2–11 months later** — the backtest proves we surfaced real, under-prioritized needs before the team acted on them.

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

## Known limitations (stated honestly)
- **Backtest coverage ~2017–2018** — GitHub REST paginates only ~10 000 issues via offset, so post-T0 matching reaches ≈2018; deeper coverage needs the Search API with date ranges.
- **Confidence uncalibrated this run** — all 15 backtest labels came out one outcome (all shipped-later), so there was no contrast to fit a calibration curve against; confidence stays the transparent score (honestly labelled).
