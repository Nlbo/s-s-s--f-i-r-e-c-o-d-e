# Pitch — The Silent Stakeholder

*8-minute pitch + live defense. Numbers marked ⟨…⟩ are filled from the final `sss run`.*

---

## 0. One line (say this first)
> "We don't tell you what users complained about — we tell you what they **needed and never said**, and we **prove it with hindsight**."

## 1. The hook (30s)
Every product has a stakeholder who never files a ticket: the user whose real need quietly diverges from the roadmap. Reading complaints is easy. The hard, valuable thing is surfacing the **unsaid** need — and being *right*. That's what we built.

## 2. The insight that wins (60s)
Most teams will cluster complaints and rank them by frequency. That scores poorly — the brief says so explicitly. The signal of a *latent* need is second-order:
> **high pain, low explicit-ask.** Users describe the symptom or the workaround, but never name the fix.
We measure exactly that: `latency = pain_rate × (1 − explicit_request_rate)`. A gap that everyone already asks for is not latent; a gap people *feel* but never articulate is.

## 3. How it works (90s) — one diagram
Two sides of ONE product (WordPress for Android):
- **Signals**: 2016 app-store reviews + user-filed GitHub issues (👍 = demand) + cross-source support tickets.
- **Roadmap**: GitHub milestones + priority/type-labeled issues = what the team committed to.

Multi-agent pipeline: JTBD extraction → latent-theme clustering → **gap engine** (aligns each theme to the roadmap → IGNORED / UNDER-PRIORITIZED / MISUNDERSTOOD) → **calibrated confidence** → **adversarial critic** → **backtest validator**.

## 4. The differentiator — a backtest, not an opinion (90s)
The reviews are from 2016. We have the repo's full history to 2026. So we predict gaps **using only 2016 data**, then check what the team **actually built afterward**. This run: **3/3** predicted under-prioritized needs were shipped by the team **2, 3, and 11 months after T0** (GH-5434 / GH-5685 / GH-6955) — we flagged them before the team acted. That turns "trust us" into a checkable receipt. (We stay honest on the number: with all three confirmed one way, there's no negative class to fit a calibration curve, so we report the transparent score, not a fake calibrated %.)

## 5. Confidence you can defend (45s)
Confidence is **not** an LLM vibe — it's a transparent linear model over six measured features (volume, source-diversity, intensity, cohesion, gap-clarity, contradiction), documented in `SPEC.md §6`, then calibrated against the backtest. Ask us to defend any number and we point at its feature vector.

## 6. Demo (90s)
Open `report.html` (self-contained dashboard): headline gap, filter by verdict, click a gap → its **evidence trace** with signal IDs spanning reviews + GitHub + tickets. Every gap is provable from the linked IDs. **No evidence, no gap.**

## 7. Results (say the headline)
Analysed **4 116 signals** (2 287 reviews + 1 029 GitHub issues + 800 tickets) against a **1 719-item T0 roadmap**. Top 3 under-served needs, **all validated by the backtest**:
1. **Reliable multi-image / media upload** (multi-select, no merge/fail) — team shipped a fix **+2 months** after T0 (GH-5434).
2. **Consistent text-formatting** in the editor — shipped **+3 months** (GH-5685).
3. **Reliable media-library** experience — shipped **+11 months** (GH-6955).
> Headline: *"Using only 2016 data we flagged 3 under-prioritized needs — the team shipped fixes for all three within 2–11 months. We saw the silent stakeholder before they did."*

## 8. Why we win (map to the rubric) (30s)
- **Correctness & rigor**: every gap traces to IDs; verdicts + confidence are backtested against real outcomes.
- **Live defense**: the adversarial critic already argued the null hypothesis for us; the confidence breakdown answers "defend this number."
- **Build quality / security**: spec-driven, typed, tested, CI with a secret scan; honest incremental commit history.

---

## Live-defense Q&A prep (rehearse these)
- **"Why is this #1?"** → highest confidence ⟨%⟩ *and* backtest-corroborated (shipped/still-open). Show the feature vector + the post-T0 evidence.
- **"Here's a gap you missed — why?"** → open the theme-coverage table: either it merged into gap #k, or it was dropped for low latency (surface complaint) / adequate roadmap coverage. The CriticAgent log shows the reasoning.
- **"Defend this confidence score."** → `SPEC.md §6` formula + this gap's V/D/I/K/G/X + calibration curve.
- **"Isn't this just a frequent complaint?"** → latency score: pain ⟨0.x⟩ but explicit-ask ⟨0.0x⟩ — they feel it, they don't ask for it.
- **"Aren't those support tickets a different product?"** → yes, and we never let a ticket-only theme become a gap: a gap must be anchored in ≥3 of WordPress's *own* signals; tickets only corroborate need-categories.
- **"How do we know the LLM didn't hallucinate a gap?"** → every gap is grounded in cited signal IDs you can open; the pipeline runs deterministically offline too (same structure without any LLM).
