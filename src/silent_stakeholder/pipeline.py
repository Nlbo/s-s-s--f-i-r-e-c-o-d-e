"""Pipeline orchestrator (SPEC.md §3).

DAG: ingest -> extract -> cluster -> gap -> confidence -> validate(backtest)
     -> calibrate -> critic -> rank -> report.
Each stage is a pure-ish function over typed models, so the whole run is reproducible
and testable. Runs fully offline via the deterministic fallback when no key is set.
"""

from __future__ import annotations

from .agents.calibrate import calibrate
from .agents.cluster import cluster_needs
from .agents.confidence import score_all
from .agents.critic import critique_all
from .agents.extract import extract_need_units
from .agents.gap import detect_gaps
from .agents.validate import validate_gaps
from .config import Settings
from .ingest.reviews import load_reviews
from .ingest.roadmap import split_github
from .ingest.tickets import load_tickets
from .llm import LLMClient
from .report import build_report, rank_and_select, write_report
from .schemas import Signal


def run(settings: Settings, *, limit: int | None = None, offline: bool = False) -> None:
    llm = LLMClient(settings, offline=offline)
    t0 = settings.analysis_t0
    # offline is truly offline: no token => shallow cached roadmap, no backtest network
    token = "" if offline else settings.github_token
    mode = "offline (deterministic fallback)" if llm.offline else f"{llm.backend}:{llm._chat_model}"

    print("The Silent Stakeholder — pipeline")
    print(f"  product : {settings.target_app_package}  ({settings.target_github_repo})")
    print(f"  T0      : {t0}   mode: {mode}")

    # 1. ingest -------------------------------------------------------------
    reviews = load_reviews(settings.target_app_package, until=t0, limit=limit)
    max_pages = None if token else 3
    roadmap_all, gh_sigs = split_github(
        settings.target_github_repo, token, created_before=t0, max_pages=max_pages,
    )
    roadmap_t0 = [r for r in roadmap_all if (r.created_at or "") <= t0]
    gh_pre = [g for g in gh_sigs if (g.date or "") <= t0]
    tickets = load_tickets(limit=settings.max_tickets)
    signals: list[Signal] = (reviews + gh_pre + tickets)[: settings.max_signals]
    print(f"  ingest  : {len(reviews)} reviews + {len(gh_pre)} gh-issues + {len(tickets)} tickets "
          f"= {len(signals)} signals | roadmap@T0 {len(roadmap_t0)} ({len(roadmap_all)} total)")
    if not token:
        print("  note    : no token this run -> shallow roadmap + backtest N/A")

    # 2-3. extract + cluster ------------------------------------------------
    units = extract_need_units(llm, signals)
    sentiment_by_id = {u.signal_id: u.sentiment for u in units}
    threshold = 0.55 if llm._embed_openai else 0.95  # dense vs TF-IDF-SVD spaces
    themes = cluster_needs(llm, units, signals, distance_threshold=threshold)
    print(f"  themes  : {len(themes)} candidate need-themes (cluster threshold {threshold})")

    # 4-5. gap + confidence -------------------------------------------------
    cands = detect_gaps(llm, themes, signals, roadmap_t0)
    gaps = score_all(settings, cands, signals, sentiment_by_id)

    # 6. validate (backtest) then 7. calibrate ------------------------------
    gaps = validate_gaps(
        llm, gaps, roadmap_all,
        repo=settings.target_github_repo, token=token, t0=t0,
    )
    calib_status, _ = calibrate(gaps)

    # 8. critic (adversarial) — adjusts the (calibrated) confidence ---------
    gaps, survives = critique_all(llm, gaps, cands, signals)

    # 9. rank + report ------------------------------------------------------
    top = rank_and_select(gaps, survives)
    meta = {
        "mode": mode,
        "n_signals": len(signals),
        "n_themes": len(themes),
        "n_roadmap": len(roadmap_t0),
        "n_candidates": len(cands),
        "calibration": calib_status,
    }
    report = build_report(settings.target_app_package, t0, top, meta)
    paths = write_report(report)

    print(f"\n  calibration: {calib_status}")
    print(f"  >> {len(top)} gaps ranked. One-liner:\n     {report.one_sentence_gap}")
    for g in top:
        print(f"     #{g.rank} [{int(g.confidence*100):>2}%] {g.verdict:<17} {g.need[:58]}")
    print("\n  artifacts:")
    for k, p in paths.items():
        print(f"     {k:4} -> {p}")
