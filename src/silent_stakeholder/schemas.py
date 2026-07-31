"""Typed data contracts (SPEC.md §8). All external/LLM data is validated through
these models — untrusted input never flows on unchecked.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SourceType = Literal["review", "gh_issue", "ticket"]
Verdict = Literal["IGNORED", "UNDER-PRIORITIZED", "MISUNDERSTOOD"]


class Signal(BaseModel):
    """One atomic piece of user voice."""

    id: str
    source: SourceType
    text: str
    date: str | None = None
    star: int | None = None          # app-store reviews
    reactions: int = 0               # github 👍 = demand weight
    url: str | None = None


class RoadmapItem(BaseModel):
    """Something the team committed to build."""

    id: str
    kind: Literal["milestone", "issue"]
    title: str
    body: str = ""
    labels: list[str] = Field(default_factory=list)
    priority: str | None = None      # e.g. "[Pri] High", "P2"
    milestone: str | None = None
    state: str = "open"
    created_at: str | None = None
    closed_at: str | None = None
    url: str | None = None


class NeedUnit(BaseModel):
    """JTBD extraction from a single signal (SPEC §4[1])."""

    signal_id: str
    job: str                          # what they're trying to accomplish
    obstacle: str                     # what blocks them
    expressed_solution: str | None = None  # did they name a fix? (None => latent-leaning)
    is_workaround: bool = False
    sentiment: float = 0.0            # -1 (angry) .. +1 (happy)
    churn_markers: list[str] = Field(default_factory=list)


class NeedTheme(BaseModel):
    """A cluster of need-units = a candidate need (SPEC §4[2])."""

    id: str
    label: str
    signal_ids: list[str] = Field(default_factory=list)
    size: int = 0
    latency: float = 0.0              # SPEC §5: pain_rate * (1 - explicit_request_rate)
    pain_rate: float = 0.0
    explicit_request_rate: float = 0.0


class EvidenceSignal(BaseModel):
    id: str
    source: SourceType
    star: int | None = None
    reactions: int = 0
    date: str | None = None
    quote: str


class RoadmapRef(BaseModel):
    id: str
    type: Literal["milestone", "issue", "none"]
    note: str = ""


class ConfidenceBreakdown(BaseModel):
    # Single-letter keys mirror the SPEC §6 formula notation on purpose.
    V: float
    D: float
    I: float  # noqa: E741 - matches SPEC confidence-formula notation
    K: float
    G: float
    X: float
    raw: float


class Validation(BaseModel):
    built_later: bool | None = None
    shipped_in: str | None = None
    lag_months: int | None = None
    still_open: bool | None = None
    reaction_growth: int | None = None
    note: str = ""


class Gap(BaseModel):
    """A ranked, proven gap — carries all four required fields (SPEC §8)."""

    rank: int
    need: str                                     # (1)
    confidence: float                             # (2)
    confidence_breakdown: ConfidenceBreakdown
    verdict: Verdict                              # (4)
    verdict_rationale: str
    latent_reasoning: str
    evidence_signals: list[EvidenceSignal] = Field(default_factory=list)  # (3)
    roadmap_refs: list[RoadmapRef] = Field(default_factory=list)
    adversarial_check: str = ""
    validation: Validation = Field(default_factory=Validation)
    theme_id: str | None = None


class Report(BaseModel):
    product: str
    generated_at: datetime
    t0: str
    one_sentence_gap: str
    gaps: list[Gap]
    meta: dict = Field(default_factory=dict)
