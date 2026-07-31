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

### [SLIDE 6 — Results]  ~75s  *(slow down — this is the peak)*
> "We analyzed **4,116 signals** against a **1,719-item** 2016 roadmap, and five latent needs came out on top — publishing that reliably works, video attachment, account-creation errors, posts loading over time, and a navigable comments experience.
> And here's the receipt. *(point at the cards)*
> The team eventually addressed **every single one** — but look how late: eight months, twenty, twenty-one, and for account-creation errors, **twenty-seven months**. We flagged all of them from 2016 data, up to more than two years before the team acted.
> And across all fifteen candidate gaps, the backtest confirmed **thirteen as genuine**. That's our precision.
> That's not an opinion — it's a backtest. And every need traces to specific signal IDs. No evidence, no gap."

### [SLIDE 7 — Confidence you can defend]  ~40s
> "Our confidence isn't a number the model made up. It's a transparent formula over six measured features — volume, source diversity, intensity, cohesion, gap-clarity, and contradiction — and the scores actually differ, from fifty to seventy-one percent.
> Ask us to defend any score and we point at its vector. Now, we could have slapped a 'calibrated' label on this — but the backtest confirmed thirteen of fifteen, which is too skewed to fit a real curve; it would just collapse every gap to one number. So we kept the honest transparent score and told you why. We'd rather be honest than impressive."

### [SLIDE 8 — Why we win]  ~35s
> "So: on **rigor**, every gap is provable and backtested. On **live defense**, our own critic already argued the other side, and the confidence breakdown answers 'defend this.' On **build quality**, it's spec-driven, typed, tested, with CI and a secret scan — and an honest, incremental commit history you can read."

### [SLIDE 9 — Closing]  ~20s
> "We saw the silent stakeholder **before the team did** — and we can prove it.
> From 2016 data, five latent needs the roadmap missed. The team fixed every one — but eight to twenty-seven months late — and the backtest confirmed thirteen of fifteen gaps as genuine.
> The repo, the runnable system, and the full evidence are right here. Thank you — we're happy to defend any gap you pick."

---

## If a judge interrupts (rapid answers)
- **"Why is #1 first?"** → Highest confidence (71%) and the strongest evidence — publishing is the core job-to-be-done, so 403s and silent failures make the whole app useless; and the team took **20 months** to even close a related issue.
- **"How can a gap be IGNORED but shipped later?"** → It can't, and we don't show that — we **reconcile with hindsight**: if the team addressed it after T0, the verdict is *UNDER-PRIORITIZED*, not *ignored*. IGNORED is reserved for needs never genuinely addressed.
- **"Defend that confidence number."** → Point at the V·D·I·K·G·X vector on slide 7 / in `report.json` — a weighted sum (weights in `SPEC.md §6`). It's the transparent score, *not* calibrated, because 13/15 corroborated is too skewed to fit a curve — and we say so.
- **"Isn't this just a frequent complaint?"** → No — its latency is high: users felt it but didn't ask for the fix. A frequent complaint scores low on latency and we drop it.
- **"That GitHub match could be a coincidence."** → Read the issue title in the note — e.g. `GH-8300 'Blog Posts List Shows Error Message When Publishing'`. Same need, closed after our T0, ≥0.50 similarity, and we say "closed a matching issue," not "shipped a feature."
- **"A gap you missed?"** → Open the theme-coverage table: it either merged into a ranked gap, or was dropped for low latency or adequate roadmap coverage — the critic log shows why.
