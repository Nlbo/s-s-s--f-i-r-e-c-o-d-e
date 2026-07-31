"""Pipeline orchestrator (SPEC.md §3).

DAG: ingest -> extract -> cluster -> gap -> confidence -> critic -> validate -> rank -> report.
Each stage is a pure-ish function over typed models, so the whole run is reproducible
and testable. Runs fully offline via the deterministic fallback when no key is set.
"""

from __future__ import annotations

from .agents.cluster import cluster_needs
from .agents.confidence import score_all
from .agents.critic import critique_all
from .agents.extract import extract_need_units
from .agents.gap import detect_gaps
from .agents.validate import validate_gaps
from .config import Settings
from .ingest.reviews import load_reviews
from .ingest.roadmap import split_github
from .llm import LLMClient
from .report import build_report, rank_and_select, write_report
from .schemas import Signal


def run(settings: Settings, *, limit: int | None = None, offline: bool = False) -> None:
    llm = LLMClient(settings, offline=offline)
    t0 = settings.analysis_t0
    mode = "offline (deterministic fallback)" if llm.offline else f"OpenAI:{settings.openai_model}"

    print("The Silent Stakeholder — pipeline")
    print(f"  product : {settings.target_app_package}  ({settings.target_github_repo})")
    print(f"  T0      : {t0}   mode: {mode}")

    # 1. ingest -------------------------------------------------------------
    reviews = load_reviews(settings.target_app_package, until=t0, limit=limit)
    max_pages = None if settings.github_token else 3
    roadmap_all, gh_sigs = split_github(
        settings.target_github_repo, settings.github_token,
        created_before=t0, max_pages=max_pages,
    )
    roadmap_t0 = [r for r in roadmap_all if (r.created_at or "") <= t0]
    gh_pre = [g for g in gh_sigs if (g.date or "") <= t0]
    signals: list[Signal] = (reviews + gh_pre)[: settings.max_signals]
    print(f"  ingest  : {len(reviews)} reviews + {len(gh_pre)} gh-issues = {len(signals)} signals "
          f"| roadmap@T0 {len(roadmap_t0)} ({len(roadmap_all)} total)")
    if not settings.github_token:
        print("  note    : no GITHUB_TOKEN -> shallow roadmap + no backtest (add one for depth)")

    # 2-3. extract + cluster ------------------------------------------------
    units = extract_need_units(llm, signals)
    themes = cluster_needs(llm, units, signals)
    print(f"  themes  : {len(themes)} candidate need-themes")

    # 4-5. gap + confidence -------------------------------------------------
    cands = detect_gaps(llm, themes, signals, roadmap_t0)
    gaps = score_all(settings, cands, signals)

    # 6. critic (adversarial) ----------------------------------------------
    gaps, survives = critique_all(llm, gaps, cands, signals)

    # 7. validate (backtest) ------------------------------------------------
    gaps = validate_gaps(
        llm, gaps, roadmap_all,
        repo=settings.target_github_repo, token=settings.github_token, t0=t0,
    )

    # 8. rank + report ------------------------------------------------------
    top = rank_and_select(gaps, survives)
    meta = {
        "mode": mode,
        "n_signals": len(signals),
        "n_themes": len(themes),
        "n_roadmap": len(roadmap_t0),
        "n_candidates": len(cands),
    }
    report = build_report(settings.target_app_package, t0, top, meta)
    paths = write_report(report)

    print(f"\n  >> {len(top)} gaps ranked. One-liner:\n     {report.one_sentence_gap}")
    for g in top:
        print(f"     #{g.rank} [{int(g.confidence*100):>2}%] {g.verdict:<17} {g.need[:60]}")
    print("\n  artifacts:")
    for k, p in paths.items():
        print(f"     {k:4} -> {p}")
