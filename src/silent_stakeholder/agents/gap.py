"""GapAgent (SPEC.md §4[3]): align each need theme to the roadmap and assign a
verdict — IGNORED / UNDER-PRIORITIZED / MISUNDERSTOOD — with cited roadmap IDs.

Coverage (how well the roadmap addresses the *need*) drives gap-clarity G = 1 - coverage,
which is the dominant feature of the confidence score (SPEC §6). Runs with an LLM judge
or a documented heuristic fallback so results are reproducible offline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np

from ..llm import LLMClient
from ..schemas import NeedTheme, RoadmapItem, RoadmapRef, Signal, Verdict

LOW = 0.30       # below this max-similarity: nothing on the roadmap is close -> IGNORED
COVERED = 0.62   # above this, with a real feature/priority item: adequately covered (drop)
_BUGISH = ("bug", "crash", "anr", "broken")
_FEATUREISH = ("enhancement", "feature", "task", "[pri]", "p1", "p2")


@dataclass
class GapCandidate:
    theme: NeedTheme
    verdict: Verdict
    coverage: float
    gap_clarity: float
    max_sim: float
    roadmap_refs: list[RoadmapRef]
    rationale: str
    need_restated: str
    latent_reasoning: str
    sample_signal_ids: list[str] = field(default_factory=list)


def _select_candidates(themes: list[NeedTheme], k: int) -> list[NeedTheme]:
    if not themes:
        return []
    max_size = max(t.size for t in themes) or 1
    scored = sorted(
        themes,
        key=lambda t: 0.6 * t.latency + 0.4 * (t.size / max_size),
        reverse=True,
    )
    return scored[:k]


def _roadmap_text(r: RoadmapItem) -> str:
    return f"{r.title}. {r.body} [{' '.join(r.labels)}]".strip()


def _theme_text(t: NeedTheme, sig_by_id: dict[str, Signal]) -> str:
    quotes = [sig_by_id[sid].text[:160] for sid in t.signal_ids[:8] if sid in sig_by_id]
    return f"{t.label}. " + " ".join(quotes)


def _heuristic_verdict(
    theme: NeedTheme, matches: list[tuple[RoadmapItem, float]]
) -> tuple[Verdict, float, str]:
    """Return (verdict, coverage, rationale) from similarity + roadmap metadata."""
    if not matches:
        return "IGNORED", 0.05, "No roadmap items available to match against."
    top, a = matches[0]
    top_labels = " ".join(top.labels).lower()
    is_bugish = any(b in top_labels or b in top.title.lower() for b in _BUGISH)
    is_feature = any(f in top_labels for f in _FEATUREISH)
    low_priority = top.priority is None or "high" not in (top.priority or "").lower()

    if a < LOW:
        return "IGNORED", round(a, 3), (
            f"Nearest roadmap item ({top.id}) is only {a:.2f} similar — the roadmap "
            "has nothing addressing this need."
        )
    if a >= COVERED and is_feature and not is_bugish:
        return "UNDER-PRIORITIZED", round(a * 0.7, 3), (
            f"Roadmap item {top.id} is related but "
            + ("low-priority/unscheduled" if low_priority else "still open")
            + " despite strong signal."
        )
    if is_bugish and not is_feature:
        return "MISUNDERSTOOD", round(a * 0.5, 3), (
            f"Roadmap treats this as a bug ({top.id}: '{top.title[:60]}') while the "
            "signal points to an unmet underlying job, not a defect."
        )
    if low_priority:
        return "UNDER-PRIORITIZED", round(a * 0.7, 3), (
            f"A related item ({top.id}) exists but is under-prioritized vs the signal strength."
        )
    return "MISUNDERSTOOD", round(a * 0.6, 3), (
        f"Roadmap item {top.id} is semantically near but frames the problem differently "
        "than users experience it."
    )


_SYS = (
    "You are a roadmap-alignment judge. Given a user NEED THEME (with sample quotes) and "
    "the most similar ROADMAP items, decide whether the roadmap IGNORES, UNDER-PRIORITIZES, "
    "or MISUNDERSTANDS the need. IGNORED = nothing addresses it. UNDER-PRIORITIZED = a related "
    "item exists but is low-priority/unscheduled vs the signal. MISUNDERSTOOD = an item looks "
    "related but solves a different framing (e.g. treats a symptom as a bug). Also restate the "
    "need in the user's terms and explain why it is latent (pain high, explicit ask low). "
    'Return JSON: {"verdict":"IGNORED|UNDER-PRIORITIZED|MISUNDERSTOOD","coverage":0..1,'
    '"roadmap_ids":[str],"rationale":str,"need_restated":str,"latent_reasoning":str}'
)


def _llm_verdict(
    llm: LLMClient, theme: NeedTheme, matches: list[tuple[RoadmapItem, float]],
    sig_by_id: dict[str, Signal],
) -> dict:
    quotes = [
        {"id": sid, "star": sig_by_id[sid].star, "text": sig_by_id[sid].text[:220]}
        for sid in theme.signal_ids[:8]
        if sid in sig_by_id
    ]
    rm = [
        {"id": r.id, "title": r.title, "priority": r.priority, "milestone": r.milestone,
         "state": r.state, "labels": r.labels}
        for r, _ in matches[:5]
    ]
    payload = {
        "theme_label": theme.label,
        "latency": theme.latency,
        "pain_rate": theme.pain_rate,
        "explicit_request_rate": theme.explicit_request_rate,
        "sample_signals": quotes,
        "nearest_roadmap": rm,
    }
    return llm.chat_json(_SYS, json.dumps(payload, ensure_ascii=False))


def detect_gaps(
    llm: LLMClient,
    themes: list[NeedTheme],
    signals: list[Signal],
    roadmap: list[RoadmapItem],
    *,
    max_candidates: int = 15,
) -> list[GapCandidate]:
    sig_by_id = {s.id: s for s in signals}
    candidates = _select_candidates(themes, max_candidates)
    if not candidates:
        return []

    theme_texts = [_theme_text(t, sig_by_id) for t in candidates]
    roadmap_texts = [_roadmap_text(r) for r in roadmap]
    joint = llm.embed(theme_texts + roadmap_texts)
    t_emb = joint[: len(candidates)]
    r_emb = joint[len(candidates):]

    out: list[GapCandidate] = []
    for i, theme in enumerate(candidates):
        if len(roadmap) == 0:
            matches: list[tuple[RoadmapItem, float]] = []
        else:
            sims = (r_emb @ t_emb[i]).astype(float)
            order = np.argsort(-sims)[:8]
            matches = [(roadmap[j], float(sims[j])) for j in order]
        max_sim = matches[0][1] if matches else 0.0

        data = _llm_verdict(llm, theme, matches, sig_by_id) if not llm.offline else {}
        if data.get("verdict") in ("IGNORED", "UNDER-PRIORITIZED", "MISUNDERSTOOD"):
            verdict: Verdict = data["verdict"]
            coverage = float(data.get("coverage", 1 - max_sim))
            rationale = str(data.get("rationale", ""))[:600]
            need_restated = str(data.get("need_restated", theme.label))[:300]
            latent_reasoning = str(data.get("latent_reasoning", ""))[:400]
            cited = set(str(x) for x in data.get("roadmap_ids", []))
            refs = [
                RoadmapRef(id=r.id, type=r.kind, note=r.title[:80])
                for r, _ in matches
                if r.id in cited
            ] or [RoadmapRef(id=r.id, type=r.kind, note=r.title[:80]) for r, _ in matches[:2]]
        else:
            verdict, coverage, rationale = _heuristic_verdict(theme, matches)
            need_restated = theme.label
            latent_reasoning = (
                f"pain_rate={theme.pain_rate:.2f} but explicit_request_rate="
                f"{theme.explicit_request_rate:.2f}: users voice the pain, rarely the fix "
                f"(latency={theme.latency:.2f})."
            )
            if verdict == "IGNORED":
                refs = [RoadmapRef(id="none", type="none", note="no matching roadmap item")]
            else:
                refs = [RoadmapRef(id=r.id, type=r.kind, note=r.title[:80]) for r, _ in matches[:2]]

        coverage = max(0.0, min(1.0, coverage))
        out.append(
            GapCandidate(
                theme=theme,
                verdict=verdict,
                coverage=round(coverage, 3),
                gap_clarity=round(max(0.05, min(0.98, 1 - coverage)), 3),
                max_sim=round(max_sim, 3),
                roadmap_refs=refs,
                rationale=rationale,
                need_restated=need_restated,
                latent_reasoning=latent_reasoning,
                sample_signal_ids=theme.signal_ids[:8],
            )
        )
    return out
