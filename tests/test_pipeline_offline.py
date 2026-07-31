"""End-to-end offline pipeline on synthetic data — the guarantees judges rely on:
every gap is typed, bounded, evidence-linked, and reproducible without a network.
"""

from __future__ import annotations

from silent_stakeholder.agents.cluster import cluster_needs
from silent_stakeholder.agents.confidence import score_all
from silent_stakeholder.agents.critic import critique_all
from silent_stakeholder.agents.extract import extract_need_units
from silent_stakeholder.agents.gap import detect_gaps
from silent_stakeholder.config import get_settings
from silent_stakeholder.llm import LLMClient
from silent_stakeholder.report import build_report, one_sentence, rank_and_select, write_report


def _run(signals, roadmap):
    s = get_settings()
    llm = LLMClient(s, offline=True)
    units = extract_need_units(llm, signals)
    themes = cluster_needs(llm, units, signals, min_size=4)
    cands = detect_gaps(llm, themes, signals, roadmap, max_candidates=10)
    gaps = score_all(s, cands, signals)
    gaps, survives = critique_all(llm, gaps, cands, signals)
    top = rank_and_select(gaps, survives, top_n=5, min_n=3)
    return s, top


def test_extract_marks_latency(signals):
    llm = LLMClient(get_settings(), offline=True)
    units = extract_need_units(llm, signals)
    assert len(units) == len(signals)
    # praise reviews are positive; pain reviews negative
    by_id = {u.signal_id: u for u in units}
    assert by_id["R-test000"].sentiment < 0        # login pain (1 star)
    assert by_id["R-test016"].sentiment > 0        # praise (5 star)


def test_pipeline_produces_valid_gaps(signals, roadmap):
    _, top = _run(signals, roadmap)
    assert 1 <= len(top) <= 5
    ids = {sg.id for sg in signals}
    for g in top:
        assert g.verdict in ("IGNORED", "UNDER-PRIORITIZED", "MISUNDERSTOOD")
        assert 0.05 <= g.confidence <= 0.95
        assert g.evidence_signals, "no evidence = not allowed (SPEC: no evidence, no gap)"
        for e in g.evidence_signals:
            assert e.id in ids                      # evidence traces to real signals
        b = g.confidence_breakdown
        # breakdown reproduces the SPEC §6 formula (tolerance covers 3-decimal rounding)
        assert abs(
            0.20 * b.V + 0.15 * b.D + 0.15 * b.I + 0.15 * b.K + 0.35 * b.G - 0.25 * b.X - b.raw
        ) < 2e-3


def test_report_writes_all_artifacts(signals, roadmap, tmp_path):
    s, top = _run(signals, roadmap)
    r = build_report(s.target_app_package, s.analysis_t0, top, {"mode": "offline"})
    assert r.one_sentence_gap and one_sentence(top)
    paths = write_report(r, out_dir=tmp_path)
    for kind in ("json", "md", "html"):
        assert paths[kind].exists() and paths[kind].stat().st_size > 0
    assert "<!doctype html>" in paths["html"].read_text().lower()


def test_ranks_are_contiguous(signals, roadmap):
    _, top = _run(signals, roadmap)
    assert [g.rank for g in top] == list(range(1, len(top) + 1))
