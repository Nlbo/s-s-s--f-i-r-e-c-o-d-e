"""Central configuration. Single source of truth for paths, budgets, and the
confidence weights defined in SPEC.md §6. Loaded from environment / .env only —
no secret is ever hard-coded here.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # read .env if present; real values never committed

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CACHE_DIR = DATA_DIR / "cache"
LLM_CACHE_DIR = ROOT / ".llm_cache"
OUT_DIR = ROOT / "out"
FIXTURES_DIR = ROOT / "tests" / "fixtures"


@dataclass(frozen=True)
class ConfidenceWeights:
    """SPEC.md §6. Positive weights over {V,D,I,K,G}; X is a penalty.

    Kept in one place so 'defend this confidence score' is answered by pointing here.
    """

    volume: float = 0.20
    diversity: float = 0.15
    intensity: float = 0.15
    cohesion: float = 0.15
    gap_clarity: float = 0.35
    contradiction_penalty: float = 0.25

    def score(
        self,
        *,
        volume: float,
        diversity: float,
        intensity: float,
        cohesion: float,
        gap_clarity: float,
        contradiction: float,
    ) -> float:
        raw = (
            self.volume * volume
            + self.diversity * diversity
            + self.intensity * intensity
            + self.cohesion * cohesion
            + self.gap_clarity * gap_clarity
            - self.contradiction_penalty * contradiction
        )
        return max(0.05, min(0.95, raw))


def _get(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


@dataclass(frozen=True)
class Settings:
    # --- LLM backends (all optional — deterministic fallback used when absent). ---
    # Auto-detected priority: Hackstudio router (LLM_KEY+LLM_URL) -> OpenAI -> offline.
    openai_api_key: str = field(default_factory=lambda: _get("OPENAI_API_KEY"))
    openai_model: str = field(default_factory=lambda: _get("OPENAI_MODEL", "gpt-4o-mini"))
    openai_embed_model: str = field(
        default_factory=lambda: _get("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    )
    # OpenAI-compatible internal router (e.g. the Hackstudio LLM gateway).
    llm_key: str = field(default_factory=lambda: _get("LLM_KEY"))
    llm_url: str = field(
        default_factory=lambda: _get("LLM_URL", "https://llm-router-qa.qa.us-west-2.aws.wfk8s.com")
    )
    llm_model: str = field(default_factory=lambda: _get("LLM_MODEL", "claude-opus-4-8"))

    github_token: str = field(default_factory=lambda: _get("GITHUB_TOKEN"))

    # Target product (override to retarget the whole system)
    target_app_package: str = field(
        default_factory=lambda: _get("TARGET_APP_PACKAGE", "org.wordpress.android")
    )
    target_github_repo: str = field(
        default_factory=lambda: _get("TARGET_GITHUB_REPO", "wordpress-mobile/WordPress-Android")
    )
    analysis_t0: str = field(default_factory=lambda: _get("ANALYSIS_T0", "2017-01-01"))

    # Budgets / guardrails
    max_signals: int = field(default_factory=lambda: int(_get("MAX_SIGNALS", "6000")))
    llm_max_concurrency: int = field(
        default_factory=lambda: int(_get("LLM_MAX_CONCURRENCY", "8"))
    )

    weights: ConfidenceWeights = field(default_factory=ConfidenceWeights)

    @property
    def backend(self) -> str:
        """'router' (internal gateway) | 'openai' | 'offline'."""
        if self.llm_key and self.llm_url:
            return "router"
        if self.openai_api_key:
            return "openai"
        return "offline"

    @property
    def use_llm(self) -> bool:
        return self.backend != "offline"


def get_settings() -> Settings:
    return Settings()


def ensure_dirs() -> None:
    for d in (DATA_DIR, RAW_DIR, CACHE_DIR, LLM_CACHE_DIR, OUT_DIR):
        d.mkdir(parents=True, exist_ok=True)
