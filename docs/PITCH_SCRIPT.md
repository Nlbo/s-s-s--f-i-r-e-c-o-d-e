# Pitch script — what to say, slide by slide

**~6–7 min. Speak in English. Slides = `docs/Silent_Stakeholder_Pitch.pptx`.**
Delivery: slow down on the backtest slide (slide 6) — that's the moment. Numbers in **bold** are the ones judges remember; say them clearly.

---

### [SLIDE 1 — Title]  ~20s
> "Hi — we're **The Silent Stakeholder**.
> Every product has a stakeholder who never files a ticket, never joins sprint planning — the user whose real need quietly drifts away from what the team is building.
> We built a system that finds those needs, in the user's own words — and proves them from the data."

*(Click to slide 2.)*

### [SLIDE 2 — The problem]  ~40s
> "Reading complaints is easy. Anyone can scrape a review and list the top gripes.
> The hard part — the valuable part — is the **latent** need: the pain a user feels but never puts into words as a feature request. They just describe a workaround, or they churn silently.
> And the brief is explicit about this: *listing frequent complaints scores poorly*. So we didn't build a complaint counter."

### [SLIDE 3 — The insight]  ~50s
> "Here's our core idea. A surface complaint is high pain where **everyone already names the fix** — cluster and count, and the biggest blob wins. That's the trap.
> A latent need is high pain where users **rarely name the fix**.
> So we measure exactly that. We call it **latency** — pain rate, times one minus the explicit-ask rate. High pain, low ask. That single number is what separates a hidden need from a loud complaint, and it drives everything downstream."

### [SLIDE 4 — How it works]  ~55s
> "We assemble two sides of one real product — WordPress for Android.
> On the signal side: **2016 app-store reviews**, user-filed GitHub issues with their thumbs-up as demand, and support tickets.
> On the roadmap side: GitHub milestones and prioritized issues — what the team actually committed to.
> Then a pipeline of agents: extract the job-to-be-done, cluster the latent themes, align each theme to the roadmap to get a verdict — ignored, under-prioritized, or misunderstood — score confidence, have an adversarial critic try to kill it, and finally backtest it. Every gap comes out with a need, a confidence, an evidence trace by ID, and a verdict. And it runs fully offline too, so it's reproducible."

### [SLIDE 5 — The differentiator]  ~50s
> "Now, anyone can claim a gap. Here's how we prove we're right.
> The reviews are from **2016**. We have the repository's entire history to today.
> So we predict the gaps using **only 2016 data** — and then we check what the team **actually shipped afterward**. Hindsight becomes our answer key."

### [SLIDE 6 — Results]  ~70s  *(slow down — this is the peak)*
> "We analyzed **4,116 signals** against a **1,719-item** 2016 roadmap. Three under-served needs came out on top: reliable multi-image upload, consistent text formatting in the editor, and the media-library experience.
> And here's the receipt. *(point at the green cards)*
> The team shipped a media-browser fix **two months** later. The editor-save fix, **three months** later. The media multi-select fix, **eleven months** later.
> We flagged all three from 2016 data — **before the team acted on them**. That's not an opinion. That's a backtest. And every one of those needs traces back to specific signal IDs — no evidence, no gap."

### [SLIDE 7 — Confidence you can defend]  ~40s
> "Our confidence isn't a number the model made up. It's a transparent formula over six measured features — volume, source diversity, intensity, cohesion, gap-clarity, and contradiction.
> Ask us to defend any score and we point at its vector. And we're disciplined about the word *calibrated*: we only say it when the backtest gives us enough labels to fit a curve — otherwise we tell you it's uncalibrated. We'd rather be honest than impressive."

### [SLIDE 8 — Why we win]  ~35s
> "So: on **rigor**, every gap is provable and backtested. On **live defense**, our own critic already argued the other side, and the confidence breakdown answers 'defend this.' On **build quality**, it's spec-driven, typed, tested, with CI and a secret scan — and an honest, incremental commit history you can read."

### [SLIDE 9 — Closing]  ~20s
> "We saw the silent stakeholder **before the team did** — and we can prove it.
> From 2016 data, three under-prioritized needs; the team shipped all three within two to eleven months.
> The repo, the runnable system, and the full evidence are right here. Thank you — we're happy to defend any gap you pick."

---

## If a judge interrupts (rapid answers)
- **"Why is #1 first?"** → Highest confidence *and* the shortest backtest lag — the team shipped it in 2 months, so the under-prioritization was real and urgent.
- **"Defend that confidence number."** → Point at the V·D·I·K·G·X vector on slide 7 / in `report.json`; it's a weighted sum, weights in `SPEC.md §6`.
- **"Isn't this just a frequent complaint?"** → No — its latency is high: users felt it but didn't ask for the fix. A frequent complaint scores low on latency and we drop it.
- **"That GitHub match could be a coincidence."** → Read the issue title in the note — `GH-5434 'Media browser fails to load images'`. It's the same need, and it closed after our T0. We also require a 0.50+ similarity.
- **"A gap you missed?"** → Open the theme-coverage table: it either merged into a ranked gap, or was dropped for low latency or adequate roadmap coverage — the critic log shows why.
- **"Why no IGNORED gaps?"** → Honest finding: WordPress is well-maintained — almost everything gets addressed eventually, just late. That's *under-prioritized*, and the backtest confirms it. On a neglected product you'd see IGNORED.
