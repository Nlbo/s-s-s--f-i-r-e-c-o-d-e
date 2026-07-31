"""Rank surviving gaps and emit the submission artifacts (SPEC.md §8):
out/report.json (machine), out/report.md and out/report.html (human), plus the
one-sentence gap statement required by the rules.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import OUT_DIR
from .schemas import Gap, Report

TEMPLATES = Path(__file__).parent / "templates"
_VERDICT_PHRASE = {
    "IGNORED": "unaddressed",
    "UNDER-PRIORITIZED": "under-prioritized",
    "MISUNDERSTOOD": "misunderstood",
}


def _corroborated(g: Gap) -> bool:
    v = g.validation
    if g.verdict == "IGNORED":
        return v.built_later is False
    return bool(v.built_later)  # UNDER/MISUNDERSTOOD confirmed if shipped late


def rank_and_select(
    gaps: list[Gap], survives: list[bool], *, top_n: int = 5, min_n: int = 3
) -> list[Gap]:
    paired = list(zip(gaps, survives, strict=True))
    survivors = [g for g, s in paired if s]
    if len(survivors) < min_n:  # never return fewer than min_n; backfill by confidence
        rest = sorted((g for g, s in paired if not s), key=lambda g: g.confidence, reverse=True)
        survivors += rest[: min_n - len(survivors)]
    survivors.sort(key=lambda g: g.confidence + (0.05 if _corroborated(g) else 0.0), reverse=True)
    top = survivors[:top_n]
    for i, g in enumerate(top, 1):
        g.rank = i
    return top


def one_sentence(top: list[Gap]) -> str:
    if not top:
        return "No gap met the evidence bar."
    g = top[0]
    need = g.need.rstrip(". ")
    return (
        f"{need} — {_VERDICT_PHRASE[g.verdict]} by the roadmap despite the evidence "
        f"({int(round(g.confidence * 100))}% confidence)."
    )


def build_report(product: str, t0: str, top: list[Gap], meta: dict) -> Report:
    return Report(
        product=product,
        generated_at=datetime.now(UTC),
        t0=t0,
        one_sentence_gap=one_sentence(top),
        gaps=top,
        meta=meta,
    )


def _to_markdown(r: Report) -> str:
    lines = [
        f"# 🔇 The Silent Stakeholder — {r.product}",
        "",
        f"*Roadmap snapshot T0 = {r.t0} · generated {r.generated_at:%Y-%m-%d %H:%M UTC} "
        f"· mode {r.meta.get('mode', '?')}*",
        "",
        "## The single most important unmet need",
        f"> **{r.one_sentence_gap}**",
        "",
        "## Ranked gaps",
    ]
    for g in r.gaps:
        b = g.confidence_breakdown
        lines += [
            "",
            f"### {g.rank}. {g.need}  ·  **{g.verdict}**  ·  confidence "
            f"**{int(round(g.confidence * 100))}%**",
            "",
            f"**Why a gap:** {g.verdict_rationale}",
            "",
            f"*Latent because:* {g.latent_reasoning}",
            "",
            f"**Confidence** = V {b.V} · D {b.D} · I {b.I} · K {b.K} · G {b.G} · X {b.X} "
            f"(raw {b.raw})",
        ]
        if g.validation and (g.validation.note or g.validation.built_later is not None):
            lines += ["", f"**Backtest:** {g.validation.note}"]
        lines += ["", f"**Evidence ({len(g.evidence_signals)} signals):**"]
        for e in g.evidence_signals:
            tag = f"★{e.star}" if e.star else (f"👍{e.reactions}" if e.reactions else "")
            lines.append(f"- `{e.id}` ({e.source} {tag}) — {e.quote}")
        refs = ", ".join(f"`{r_.id}`" for r_ in g.roadmap_refs)
        lines += [f"\n**Roadmap refs:** {refs}", f"\n*Adversarial check:* {g.adversarial_check}"]
    return "\n".join(lines) + "\n"


def write_report(r: Report, out_dir: Path = OUT_DIR) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    paths["json"] = out_dir / "report.json"
    paths["json"].write_text(r.model_dump_json(indent=2))

    paths["md"] = out_dir / "report.md"
    paths["md"].write_text(_to_markdown(r))

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    paths["html"] = out_dir / "report.html"
    paths["html"].write_text(env.get_template("report.html.j2").render(report=r))
    return paths
