"""Ingest the GitHub side of one product (SPEC.md §2).

Splits GitHub into two populations, with a documented, traceable rule:
  * ROADMAP item  = milestone, or an issue on a milestone / carrying a priority
    label ([Pri] High, P1/P2)  -> "what the team committed to build"
  * USER SIGNAL   = any other user-filed issue (feature request / bug / crash)
    with its 👍 reaction count as a quantitative demand weight.

Responses are cached to data/raw/github (gitignored) so re-runs are free and the
unauthenticated 60 req/h limit isn't a blocker during development. A GITHUB_TOKEN
lifts the limit to 5000/h for the full historical pull.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests

from ..config import RAW_DIR
from ..ids import issue_id, milestone_id
from ..schemas import RoadmapItem, Signal

API = "https://api.github.com"
_PRIORITY_HINTS = ("[pri]", "p1", "p2", "priority")


class GitHubClient:
    def __init__(self, repo: str, token: str = "", cache_dir: Path | None = None) -> None:
        self.repo = repo
        self.cache = (cache_dir or (RAW_DIR / "github" / repo.replace("/", "__")))
        self.cache.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _get(self, path: str, params: dict, cache_key: str) -> list[dict]:
        cf = self.cache / f"{cache_key}.json"
        if cf.exists():
            return json.loads(cf.read_text())
        r = self.session.get(f"{API}{path}", params=params, timeout=60)
        if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(r.headers.get("X-RateLimit-Reset", "0"))
            raise RuntimeError(
                f"GitHub rate limit hit. Set GITHUB_TOKEN for 5000/h "
                f"(resets ~{max(0, reset - int(time.time()))}s)."
            )
        # GitHub caps deep listing pagination (~page 100) with a 422 — treat any 422
        # as "no more results" so a long history walk ends cleanly instead of crashing.
        if r.status_code == 422:
            return []
        r.raise_for_status()
        data = r.json()
        cf.write_text(json.dumps(data))
        return data

    def milestones(self) -> list[RoadmapItem]:
        out: list[RoadmapItem] = []
        for page in range(1, 6):  # 500 milestones max; plenty
            batch = self._get(
                f"/repos/{self.repo}/milestones",
                {"state": "all", "per_page": 100, "page": page},
                f"milestones_p{page}",
            )
            if not batch:
                break
            for m in batch:
                out.append(
                    RoadmapItem(
                        id=milestone_id(m["title"]),
                        kind="milestone",
                        title=m["title"],
                        body=m.get("description") or "",
                        state=m.get("state", "open"),
                        created_at=m.get("created_at"),
                        closed_at=m.get("closed_at"),
                        milestone=m["title"],
                        url=m.get("html_url"),
                    )
                )
        return out

    def issues(
        self, *, created_before: str | None = None, max_pages: int | None = None
    ) -> list[dict]:
        """Raw issues, oldest first (so the historical era comes first). Stops early
        once created_at passes `created_before`. PRs are filtered out."""
        raw: list[dict] = []
        page = 1
        while True:
            if max_pages and page > max_pages:
                break
            batch = self._get(
                f"/repos/{self.repo}/issues",
                {
                    "state": "all",
                    "per_page": 100,
                    "page": page,
                    "sort": "created",
                    "direction": "asc",
                },
                f"issues_asc_p{page}",
            )
            if not batch:
                break
            stop = False
            for it in batch:
                if "pull_request" in it:
                    continue
                if created_before and it.get("created_at", "") >= created_before:
                    stop = True
                    break
                raw.append(it)
            if stop:
                break
            page += 1
        return raw


def _is_roadmap(issue: dict) -> bool:
    if issue.get("milestone"):
        return True
    for lb in issue.get("labels", []):
        name = (lb["name"] if isinstance(lb, dict) else str(lb)).lower()
        if any(h in name for h in _PRIORITY_HINTS):
            return True
    return False


def _priority(issue: dict) -> str | None:
    for lb in issue.get("labels", []):
        name = lb["name"] if isinstance(lb, dict) else str(lb)
        if any(h in name.lower() for h in _PRIORITY_HINTS):
            return name
    return None


def split_github(
    repo: str,
    token: str = "",
    *,
    created_before: str | None = None,
    max_pages: int | None = None,
) -> tuple[list[RoadmapItem], list[Signal]]:
    """Return (roadmap_items, user_signal_issues)."""
    gh = GitHubClient(repo, token)
    roadmap: list[RoadmapItem] = gh.milestones()
    signals: list[Signal] = []
    for it in gh.issues(created_before=created_before, max_pages=max_pages):
        labels = [(lb["name"] if isinstance(lb, dict) else str(lb)) for lb in it.get("labels", [])]
        if _is_roadmap(it):
            roadmap.append(
                RoadmapItem(
                    id=issue_id(it["number"]),
                    kind="issue",
                    title=it.get("title", ""),
                    body=(it.get("body") or "")[:4000],
                    labels=labels,
                    priority=_priority(it),
                    milestone=(it.get("milestone") or {}).get("title"),
                    state=it.get("state", "open"),
                    created_at=it.get("created_at"),
                    closed_at=it.get("closed_at"),
                    url=it.get("html_url"),
                )
            )
        else:
            signals.append(
                Signal(
                    id=issue_id(it["number"]),
                    source="gh_issue",
                    text=f"{it.get('title', '')}. {(it.get('body') or '')[:1500]}",
                    date=(it.get("created_at") or "")[:10] or None,
                    reactions=(it.get("reactions") or {}).get("total_count", 0),
                    url=it.get("html_url"),
                )
            )
    return roadmap, signals
