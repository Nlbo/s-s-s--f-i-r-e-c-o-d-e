# The Silent Stakeholder — Specification

> Spec-driven anchor. Everything in the codebase must trace back to a clause here.
> If code and spec disagree, one of them is a bug.

**Firecode Hackathon · Problem: THE SILENT STAKEHOLDER**
**Product under analysis:** WordPress for Android (`org.wordpress.android` / GitHub `wordpress-mobile/WordPress-Android`)

---

## 0. One-sentence mission

Surface the **top 3–5 latent, unspoken user needs** that the product roadmap is **missing or under-serving**, and **prove each one from the data** — with a calibrated confidence score, a full evidence trace by ID, and a gap verdict.

Not a summarizer. Listing frequent complaints scores poorly. The value is inferring **latent** needs — the ones that only show up as *second-order* patterns (users describe a pain or a workaround, but never name the solution).

---

## 1. Definitions (shared vocabulary)

- **Signal** — one atomic piece of user voice with a stable ID. Sources: `review` (app-store), `gh_issue` (user-filed GitHub issue + 👍 reactions = demand), `ticket` (support ticket).
- **Roadmap item** — one thing the team *committed to build*: a GitHub milestone, or an issue that is on a milestone / labeled as accepted work (`[Type] Enhancement`, `[Type] Task`) with a priority label (`[Pri] High`, `P2`). Distinct from user-filed *requests*.
- **Need** — a job the user is trying to get done (Jobs-To-Be-Done framing), phrased in the user's terms — not a feature name.
- **Gap** — a need that the roadmap does not address, or addresses wrongly.
- **Latent need** — a need with **high pain signal but low explicit-request rate**: users describe the symptom / workaround, but rarely ask for the actual solution. Latency is measured, not asserted (see §5).
- **Verdict** — one of:
  - `IGNORED` — strong user signal, *no* roadmap item addresses it.
  - `UNDER-PRIORITIZED` — a roadmap item exists but is low-priority / far-milestone / stale relative to signal strength.
  - `MISUNDERSTOOD` — a roadmap item *looks* related but solves a different framing than what users actually need.

---

## 2. Data sources & provenance (all from the provided open datasets)

| Side | Source | Use |
|---|---|---|
| Signals | `sealuzh/app_reviews` (HF) filtered to `org.wordpress.android` | Primary user voice (has `review`, `star`, `date`) |
| Signals | `wordpress-mobile/WordPress-Android` GitHub **user-filed issues** + reaction counts | Same-product demand signal; reactions = quantitative demand |
| Signals | `Tobi-Bueck/customer-support-tickets` + `mirzayasirabdullah07/...` (HF/Kaggle) | Cross-source corroboration where topically relevant (publishing/website/CMS/app) |
| Roadmap | `wordpress-mobile/WordPress-Android` GitHub **milestones + labeled/prioritized issues** | What the team was building |

**Every signal and roadmap item keeps its source ID** (`R-*`, `GH-*`, `GH-M-*`, `T-*`) so evidence is traceable. **No evidence, no gap.**

### 2.1 Temporal design (this is a differentiator)
The app-store reviews are historical (~2016). We exploit this:
- **T0 = `ANALYSIS_T0` (default 2017-01-01).** We reconstruct the roadmap *as it stood at T0* (milestones + issues open/planned at that time).
- We detect gaps using **only signals up to T0** and the **T0 roadmap**.
- We then **backtest** predictions against the *real* post-T0 history (2017→today): did the team eventually build it? how late? is it still an open, upvoted issue? (see §7). This converts "trust our judgment" into an empirical, defensible result.

---

## 3. Architecture — a multi-agent pipeline

Orchestrated, explainable agents. Each stage has a single responsibility, typed I/O, and a cache. The orchestrator runs them as a DAG and records a decision log.

```
        ┌── ingest ──┐
reviews │            │
issues  │→ Signals ──┼──► [1] ExtractorAgent  (JTBD need-units, expressed-vs-implied)
tickets │            │            │
        └────────────┘            ▼
                          [2] ClusterAgent  (embed + cluster → need themes)
                                   │
milestones ─► Roadmap ─────────────┤
labels/prio                        ▼
                          [3] GapAgent  (RAG align theme↔roadmap → IGNORED/UNDER/MISUNDERSTOOD)
                                   │
                                   ▼
                          [4] ConfidenceAgent  (explicit calibrated formula, §6)
                                   │
                                   ▼
                          [5] CriticAgent  (adversarial: try to falsify each gap)
                                   │
                                   ▼
                          [6] ValidatorAgent  (backtest vs post-T0 history, §7)
                                   │
                                   ▼
                          Ranker → report.json + report.md + one-sentence gap
```

Agents are LLM-backed (OpenAI) with a **deterministic local fallback** (TF-IDF embeddings + rule-based extraction) so the system runs and is testable without a key.

---

## 4. Methodology per stage

**[1] Extraction (JTBD).** Each signal → `{job, obstacle, expressed_solution?, is_workaround, sentiment, churn_markers}`. Latency is born here: we separate *what the user is trying to do* from *what they literally asked for*.

**[2] Clustering.** Embed need-units; cluster into **need themes** (HDBSCAN-style density / agglomerative). Each theme aggregates its member signal IDs. Themes, not raw complaints, are the unit of analysis.

**[3] Gap engine.** For each theme, retrieve nearest roadmap items (embedding similarity). An LLM judge assigns the verdict with cited roadmap IDs and a rationale. Well-covered themes are dropped (not gaps).

**[5] Adversarial critic.** For each surviving gap, a critic argues the *null hypothesis* ("this is just a frequent complaint" / "roadmap item X already covers it" / "evidence is cherry-picked / sarcastic"). Gaps that survive falsification score higher; the critique is stored (fuel for live defense).

**[6] Ranking.** Sort by evidence strength (confidence × validation), strongest first. Keep top 3–5.

---

## 5. Latent-need scoring

For a theme, define **latency** `L`:

```
L = pain_rate * (1 - explicit_request_rate)
```
- `pain_rate` = share of member signals with negative sentiment / churn markers / low star.
- `explicit_request_rate` = share of member signals that *name a concrete solution/feature*.

High `L` = users hurt but don't articulate the fix → genuinely latent. Surfaced complaints (everyone names the fix) get low `L` and are de-prioritized. This operationalizes the rubric's core ("what users needed and never said").

---

## 6. Confidence model (calibrated, not decorative)

Confidence is a **transparent linear model over measurable features**, not an LLM vibe. For each gap:

| Feature | Meaning | Weight |
|---|---|---|
| `V` volume | log-scaled count of distinct linked signals, normalized | 0.20 |
| `D` diversity | # distinct source types (review / gh_issue / ticket) ÷ 3 | 0.15 |
| `I` intensity | mean churn/negativity/low-star intensity | 0.15 |
| `K` cohesion | 1 − normalized embedding dispersion of the theme | 0.15 |
| `G` gap clarity | how confidently roadmap alignment says it's uncovered (retrieval margin + judge) | 0.35 |
| `X` contradiction | share of signals asking for the *opposite* (penalty) | −0.25 |

```
raw = 0.20V + 0.15D + 0.15I + 0.15K + 0.35G − 0.25X
confidence = clip(raw, 0.05, 0.95)
```

- Weights are documented and tunable in one place (`config`). `G` dominates because a *roadmap* gap is fundamentally about roadmap absence.
- **Calibration:** when backtest labels exist (§7), fit a monotonic/logistic map from `raw`→observed-correctness so the reported % is empirically meaningful. 90%-sure and 55%-sure then *actually* differ.
- Every gap ships its **feature breakdown**, so "defend this score" is answered by pointing at the vector.

---

## 7. Validation / backtest (empirical proof)

Using post-T0 GitHub history as ground truth for each predicted gap:
- `built_later` + `shipped_in` + `lag_months` — did the team ship it, how late? (confirms `UNDER-PRIORITIZED`).
- `still_open` + `reaction_growth` — still an open, upvoted issue years later? (confirms `IGNORED`).
- `rebuilt/complaints_persist` — shipped but users kept asking? (confirms `MISUNDERSTOOD`).

Produces a precision figure and a calibration curve. **This is our headline rigor claim.**

---

## 8. Output contract

`out/report.json` (machine-readable) + `out/report.md` + `out/report.html` (human). Each gap carries **all four required fields** plus traces:

```jsonc
{
  "product": "org.wordpress.android",
  "generated_at": "<iso>",
  "t0": "2017-01-01",
  "one_sentence_gap": "<single most important unmet need, one line>",
  "gaps": [{
    "rank": 1,
    "need": "<in the user's terms>",                    // (1) THE NEED
    "confidence": 0.82,                                  // (2) CALIBRATED CONFIDENCE
    "confidence_breakdown": {"V":..,"D":..,"I":..,"K":..,"G":..,"X":..},
    "verdict": "UNDER-PRIORITIZED",                      // (4) GAP VERDICT
    "verdict_rationale": "...",
    "latent_reasoning": "why unsaid, not a surface complaint (L=..)",
    "evidence": {                                        // (3) EVIDENCE TRACE by ID
      "signals": [{"id":"R-00123","source":"review","star":2,"date":"...","quote":"..."},
                  {"id":"GH-4521","source":"gh_issue","reactions":34,"quote":"..."}],
      "roadmap_refs": [{"id":"GH-M-2.7","type":"milestone","note":"nothing addresses X"}]
    },
    "adversarial_check": "survived: rejected alt-explanation Y because ...",
    "validation": {"built_later": true, "shipped_in": "v8.2", "lag_months": 26, "still_open": null}
  }]
}
```

---

## 9. Security standards (audits are part of scoring)

- **Secrets**: only via env / `.env` (gitignored). Never logged, never committed. CI runs a secret scan. No credential ever printed.
- **Input handling**: all external data (reviews, issues, LLM output) treated as untrusted — validated with pydantic, no `eval`/`exec`, no shell interpolation of data, HTML output escaped (Jinja autoescape).
- **Network**: pinned dependencies from public PyPI; HTTPS only; timeouts + retries with backoff; GitHub token read-only.
- **LLM safety**: outputs are parsed/validated, never executed; prompt-injection from ingested text cannot trigger tool actions.
- **Least privilege**: the optional "file issues" action requires an explicit, separately-scoped token and human confirmation, and targets only a designated repo.

## 10. Quality standards
Typed (pydantic), linted (ruff incl. bandit security rules), tested (pytest on fixtures — no network in tests), CI on every push. Deterministic fallback keeps the whole pipeline reproducible.

## 11. Agentic dev process (how this repo is built)
Spec → implement → **self-review** (`/code-review`) → **check** (ruff + pytest) → **commit** → push. Small, honest, frequent commits (the rules reward a visible build; force-push/backdating is cheating and forbidden). A `docs/DECISION_LOG.md` records which agent did what and why.

## 12. Execution milestones
1. Foundation: spec, scaffold, CI, security config. ✅ in progress
2. Ingestion (reviews + roadmap + tickets) with fixtures.
3. Extraction + clustering.
4. Gap engine + confidence.
5. Critic + ranking + report (JSON/MD/HTML).
6. Backtest validation.
7. Dashboard (evidence explorer).
8. Digital-stakeholder issue drafting (opt-in).
9. Pitch deck.

## 13. Live-defense readiness (anticipated judge questions)
- *"Why rank this #1?"* → confidence feature vector + backtest outcome.
- *"Here's a gap you missed — why?"* → CriticAgent log + theme coverage table (we can show why a theme was dropped/merged).
- *"Defend this confidence."* → §6 breakdown + calibration curve from §7.
- *"Isn't this just a frequent complaint?"* → latency score `L` (§5) shows pain-high / explicit-ask-low.
