"""ValidatorAgent (SPEC.md §7): backtest each predicted gap against what the team
*actually did* after T0. Because the reviews are historical, we have hindsight —
this turns "trust our judgment" into a measured outcome.

For each gap we search post-T0 issue history for a semantic match:
  * matched & closed -> built_later=True, lag = T0 -> close   (confirms UNDER-PRIORITIZED)
  * matched & open   -> still_open=True, reaction_growth=👍   (confirms IGNORED demand)
  * no match         -> built_later=False                     (consistent with IGNORED)
Degrades honestly to "insufficient history" when there is no post-T0 issue corpus
(e.g. no GITHUB_TOKEN). Paging is bounded and 422-safe, so it never crashes the run.
"""

from __future__ import annotations

from datetime import date

from ..ids import issue_id
from ..ingest.roadmap import GitHubClient
from ..llm import LLMClient
from ..schemas import Gap, RoadmapItem, Validation

MIN_CORPUS = 20
FUTURE_MAX_PAGES = 200  # bounded deep walk; 422/empty stops earlier


def _months_between(a: str | None, b: str | None) -> int | None:
    try:
        da = date.fromisoformat((a or "")[:10])
        db = date.fromisoformat((b or "")[:10])
    except ValueError:
        return None
    return max(0, (db.year - da.year) * 12 + (db.month - da.month))


def build_future_corpus(
    repo: str, token: str, t0: str, roadmap: list[RoadmapItem]
) -> list[RoadmapItem]:
    """Issue-level items created strictly after T0 (what was actually built/planned later).
    Only issues count — version-number milestones carry no feature semantics. Requires a
    token for the deep walk; without one this is ~empty and the backtest reports N/A."""
    future = [r for r in roadmap if (r.created_at or "") > t0 and r.kind == "issue"]
    if not token:
        return future
    gh = GitHubClient(repo, token)
    for it in gh.issues(created_before=None, max_pages=FUTURE_MAX_PAGES):
        if (it.get("created_at") or "") <= t0:
            continue
        labels = [
            (lb["name"] if isinstance(lb, dict) else str(lb)) for lb in it.get("labels", [])
        ]
        future.append(
            RoadmapItem(
                id=issue_id(it["number"]),
                kind="issue",
                title=it.get("title", ""),
                body=(it.get("body") or "")[:1500],
                labels=labels,
                state=it.get("state", "open"),
                created_at=it.get("created_at"),
                closed_at=it.get("closed_at"),
                reactions=(it.get("reactions") or {}).get("total_count", 0),
                url=it.get("html_url"),
            )
        )
    return future


def validate_gaps(
    llm: LLMClient,
    gaps: list[Gap],
    roadmap: list[RoadmapItem],
    *,
    repo: str,
    token: str,
    t0: str,
) -> list[Gap]:
    future = build_future_corpus(repo, token, t0, roadmap)
    if len(future) < MIN_CORPUS:
        for g in gaps:
            g.validation = Validation(
                note=f"backtest N/A: only {len(future)} post-T0 issues available "
                "(set GITHUB_TOKEN for the full hindsight check)."
            )
        return gaps

    # thresholds depend on the embedding space (OpenAI dense vs TF-IDF-SVD sparse)
    match_thr = 0.42 if llm._embed_openai else 0.28

    fut_texts = [f"{r.title}. {r.body}" for r in future]
    need_texts = [
        f"{g.need}. " + (g.evidence_signals[0].quote if g.evidence_signals else "")
        for g in gaps
    ]
    joint = llm.embed(need_texts + fut_texts)
    n_emb = joint[: len(gaps)]
    f_emb = joint[len(gaps):]

    for i, g in enumerate(gaps):
        sims = (f_emb @ n_emb[i]).astype(float)
        j = int(sims.argmax())
        best, sim = future[j], float(sims[j])
        if sim < match_thr:
            g.validation = Validation(
                built_later=False, still_open=True,
                note=f"No post-T0 issue matches (best sim {sim:.2f}) — consistent with IGNORED.",
            )
        elif best.state == "closed" and best.closed_at:
            g.validation = Validation(
                built_later=True,
                shipped_in=f"{best.id}: {best.title[:60]}",
                lag_months=_months_between(t0, best.closed_at),
                still_open=False,
                note=f"Team later shipped {best.id} (closed {best.closed_at[:10]}, sim {sim:.2f}).",
            )
        else:  # matched but still open years later = acknowledged, not delivered
            g.validation = Validation(
                built_later=False, still_open=True,
                reaction_growth=best.reactions or None,
                note=(
                    f"Acknowledged as {best.id} but still OPEN "
                    f"({best.reactions}👍, sim {sim:.2f}) — demand persisted."
                ),
            )
    return gaps
