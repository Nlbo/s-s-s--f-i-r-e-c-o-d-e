"""ValidatorAgent (SPEC.md §7): backtest each predicted gap against what the team
*actually did* after T0. Because the reviews are historical, we have hindsight —
this turns "trust our judgment" into a measured outcome and is the headline rigor claim.

For each gap we search the post-T0 roadmap history (milestones + issues created after
T0) for a semantic match:
  * matched & closed  -> built_later=True, lag = T0 -> close (confirms UNDER-PRIORITIZED)
  * matched & open    -> still_open=True (planned late / never finished)
  * no match          -> built_later=False (confirms IGNORED)
Degrades honestly when post-T0 history is thin (set GITHUB_TOKEN for the full pull).
"""

from __future__ import annotations

from datetime import date

from ..ids import issue_id
from ..ingest.roadmap import GitHubClient
from ..llm import LLMClient
from ..schemas import Gap, RoadmapItem, Validation

MATCH = 0.45
MIN_CORPUS = 20


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
    """Descriptive roadmap/issue items created strictly after T0 (what was built/planned
    later). Bare version-number milestones (empty body) are excluded — they carry no
    feature semantics to match against, and counting them would fake a backtest."""
    future = [
        r
        for r in roadmap
        if (r.created_at or "") > t0 and (r.kind == "issue" or len(r.body) > 30)
    ]
    # A token enables the deep post-T0 issue pull that makes the backtest strong.
    if token:
        gh = GitHubClient(repo, token)
        for it in gh.issues(created_before=None):
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
                note=f"insufficient post-T0 history ({len(future)} items); "
                "set GITHUB_TOKEN for the full backtest."
            )
        return gaps

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
        best = future[j]
        if float(sims[j]) < MATCH:
            g.validation = Validation(
                built_later=False,
                still_open=True,
                note=f"No post-T0 item matches (best={sims[j]:.2f}); consistent with IGNORED.",
            )
            continue
        closed = best.state == "closed" and best.closed_at
        g.validation = Validation(
            built_later=bool(closed),
            shipped_in=best.title[:80] if closed else None,
            lag_months=_months_between(t0, best.closed_at) if closed else None,
            still_open=not closed,
            note=(
                f"Matched post-T0 item {best.id} ('{best.title[:50]}', {best.state}, "
                f"sim={sims[j]:.2f})."
            ),
        )
    return gaps
