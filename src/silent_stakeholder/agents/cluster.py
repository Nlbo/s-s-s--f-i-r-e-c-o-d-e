"""ClusterAgent (SPEC.md §4[2], §5): group need-units into candidate need themes
and compute the latency score that separates latent needs from surface complaints.
"""

from __future__ import annotations

import re
from collections import Counter

import numpy as np
from sklearn.cluster import AgglomerativeClustering

from ..ids import stable_id
from ..llm import LLMClient
from ..schemas import NeedTheme, NeedUnit, Signal

_WORD = re.compile(r"[a-z][a-z']+")
_STOP = set(
    "the a an and or but to of for in on with is it this that i you app my me not no so "
    "very just have has had do does did be been are was were will would can cant cannot "
    "get got make made use used using when what why how they them their there here your "
    "wordpress please really about all any more most some such only than then too "
    "one two also new now even much many way really thing things".split()
)


def _need_text(nu: NeedUnit, sig: Signal) -> str:
    parts = [nu.job, nu.obstacle, nu.expressed_solution or ""]
    joined = " ".join(p for p in parts if p).strip()
    return joined or sig.text


def _label(texts: list[str], k: int = 4) -> str:
    counts: Counter[str] = Counter()
    for t in texts:
        for w in _WORD.findall(t.lower()):
            if w not in _STOP and len(w) > 2:
                counts[w] += 1
    return " / ".join(w for w, _ in counts.most_common(k)) or "misc"


def cluster_needs(
    llm: LLMClient,
    units: list[NeedUnit],
    signals: list[Signal],
    *,
    distance_threshold: float = 0.95,
    min_size: int = 5,
) -> list[NeedTheme]:
    if not units:
        return []
    sig_by_id = {s.id: s for s in signals}
    texts = [_need_text(nu, sig_by_id[nu.signal_id]) for nu in units]
    emb = llm.embed(texts)

    if len(units) == 1:
        labels = np.array([0])
    else:
        model = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=distance_threshold,
            metric="cosine",
            linkage="average",
        )
        labels = model.fit_predict(emb)

    themes: list[NeedTheme] = []
    for cl in sorted(set(labels.tolist())):
        idx = [i for i, la in enumerate(labels) if la == cl]
        if len(idx) < min_size:
            continue
        members = [units[i] for i in idx]
        sig_ids = [m.signal_id for m in members]
        pain = 0
        explicit = 0
        for m in members:
            sig = sig_by_id[m.signal_id]
            low_star = sig.star is not None and sig.star <= 2
            is_pain = m.sentiment < 0 or bool(m.churn_markers) or low_star
            pain += int(is_pain)
            explicit += int(m.expressed_solution is not None)
        n = len(members)
        pain_rate = pain / n
        explicit_rate = explicit / n
        # cohesion = mean cosine of members to their (normalized) centroid; embeddings
        # are already L2-normalized so this is just mean dot-product to the centroid.
        sub = emb[idx]
        centroid = sub.mean(axis=0)
        cnorm = np.linalg.norm(centroid)
        cohesion = float((sub @ centroid).mean() / cnorm) if cnorm > 0 else 0.0
        themes.append(
            NeedTheme(
                id=stable_id("TH-", *sorted(sig_ids)[:5], cl, length=6),
                label=_label([texts[i] for i in idx]),
                signal_ids=sig_ids,
                size=n,
                pain_rate=round(pain_rate, 3),
                explicit_request_rate=round(explicit_rate, 3),
                latency=round(pain_rate * (1 - explicit_rate), 3),
                cohesion=round(max(0.0, min(1.0, cohesion)), 3),
            )
        )
    themes.sort(key=lambda t: (t.latency, t.size), reverse=True)
    return themes
