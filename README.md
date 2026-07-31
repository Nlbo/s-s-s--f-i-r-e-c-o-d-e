# 🔇 The Silent Stakeholder

> Every product has a stakeholder who never files a ticket, never joins sprint planning: the user whose real need quietly diverges from what the team is building. This system finds those needs — **and proves them from the data.**

**Firecode Hackathon submission.** Full spec: [`SPEC.md`](SPEC.md) · submission packet: [`SUBMISSION.md`](SUBMISSION.md) · pitch: [`docs/PITCH.md`](docs/PITCH.md) · sample output: [`docs/sample/report.md`](docs/sample/report.md).

> **Headline result (WordPress for Android):** from **2016-only** signals we surfaced 3 under-prioritized needs — reliable multi-image upload, consistent text formatting, and the media-library experience. The **backtest proves it**: the team shipped fixes for all three **2–11 months later** (GH-5434 / GH-5685 / GH-6955). We saw the silent stakeholder before they did.

## What it does
Given **one product** (WordPress for Android), it reads two sides — **what the team is building** (GitHub roadmap: milestones + prioritized issues) and **what users are signaling** (app-store reviews + user-filed issues + support tickets) — and surfaces the **top 3–5 latent, unspoken needs** the roadmap is missing or under-serving.

It is **not a complaint summarizer.** For every gap it outputs the four required things:

1. **The need** — in the user's terms
2. **A confidence score** — a transparent formula, not a vibe; and *calibrated* against the backtest when there are enough hindsight labels (otherwise honestly marked "uncalibrated") ([§6](SPEC.md#6-confidence-model-calibrated-not-decorative))
3. **An evidence trace** — every gap links to specific signal IDs. *No evidence, no gap.*
4. **A gap verdict** — `IGNORED` / `UNDER-PRIORITIZED` / `MISUNDERSTOOD`

**Differentiator:** reviews are historical (~2016), so we **backtest** every prediction against what the team *actually built* in 2017→today. Trust becomes a measured precision number.

## Architecture
A multi-agent pipeline (extractor → cluster → gap engine → confidence → adversarial critic → validator → ranker). See [`SPEC.md §3`](SPEC.md#3-architecture--a-multi-agent-pipeline).

## Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # or: pip install -r requirements.txt
cp .env.example .env             # add OPENAI_API_KEY (optional) + GITHUB_TOKEN (optional)
sss run                          # full pipeline -> out/report.{json,md,html}
```
The pipeline runs **end-to-end without any API key** using a deterministic local fallback (TF-IDF + rules); set `OPENAI_API_KEY` for best-quality extraction and judging.

## Security & quality
Secrets only via gitignored `.env`; untrusted-input validation everywhere; HTML output escaped; ruff (with bandit rules) + pytest in CI. See [`SPEC.md §9–10`](SPEC.md#9-security-standards-audits-are-part-of-scoring).

## Repo layout
```
SPEC.md                     the anchor spec
src/silent_stakeholder/     pipeline + agents + CLI
tests/                      pytest on committed fixtures (no network)
docs/DECISION_LOG.md        who (which agent) did what, and why
out/                        generated reports (gitignored)
```
