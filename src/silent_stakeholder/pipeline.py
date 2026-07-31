"""Pipeline orchestrator (SPEC.md §3).

Runs the agent DAG:
  ingest -> extract -> cluster -> gap -> confidence -> critic -> validate -> rank -> report

Stages are added incrementally; each is a pure function over typed models so the
whole thing stays testable and reproducible. This module wires them together.
"""

from __future__ import annotations

from .config import Settings


def run(settings: Settings, *, limit: int | None = None, offline: bool = False) -> None:
    mode = "offline (deterministic fallback)" if offline or not settings.use_llm else "OpenAI"
    print("The Silent Stakeholder — pipeline")
    print(f"  product : {settings.target_app_package}  ({settings.target_github_repo})")
    print(f"  T0      : {settings.analysis_t0}")
    print(f"  mode    : {mode}")
    print(f"  budget  : max_signals={settings.max_signals}" + (f", limit={limit}" if limit else ""))
    # Stages are wired here as they land (SPEC §12). Ingestion is next.
    raise SystemExit(
        "Pipeline stages are being implemented incrementally — run individual "
        "ingestion steps for now (see SPEC.md §12)."
    )
