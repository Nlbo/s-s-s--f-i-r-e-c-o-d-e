"""GitHub client + backtest-gating must degrade safely, never crash (SPEC §7).

The reviewer found an unbounded pager that died on GitHub's page-100 422; these lock
in the fix and the honest "N/A" path — without touching the network.
"""

from __future__ import annotations

from silent_stakeholder.agents.validate import validate_gaps
from silent_stakeholder.config import get_settings
from silent_stakeholder.ingest.roadmap import GitHubClient
from silent_stakeholder.llm import LLMClient
from silent_stakeholder.schemas import ConfidenceBreakdown, Gap, Validation


class _FakeResp:
    def __init__(self, status: int, payload=None):
        self.status_code = status
        self.headers: dict[str, str] = {}
        self._payload = payload if payload is not None else []

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise AssertionError(f"raise_for_status called on {self.status_code}")


def test_422_is_treated_as_end_of_results(monkeypatch, tmp_path):
    gh = GitHubClient("owner/repo", cache_dir=tmp_path / "c")
    monkeypatch.setattr(gh.session, "get", lambda *a, **k: _FakeResp(422))
    assert gh._get("/x", {}, "k") == []           # no crash, no raise_for_status
    assert gh.issues(created_before=None, max_pages=5) == []  # pager terminates cleanly


def _gap() -> Gap:
    return Gap(
        rank=0, need="n", confidence=0.5,
        confidence_breakdown=ConfidenceBreakdown(V=0, D=0, I=0, K=0, G=0, X=0, raw=0.5),
        verdict="IGNORED", verdict_rationale="", latent_reasoning="",
    )


def test_backtest_reports_na_without_a_token(tmp_path):
    llm = LLMClient(get_settings(), offline=True)
    gaps = validate_gaps(llm, [_gap()], roadmap=[], repo="owner/repo", token="", t0="2017-01-01")
    v = gaps[0].validation
    assert isinstance(v, Validation)
    assert v.built_later is None and "N/A" in v.note   # honest, not a fake verdict
