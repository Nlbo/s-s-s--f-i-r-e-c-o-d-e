"""Stable, deterministic IDs so evidence traces are reproducible across runs.

Prefixes: R- review, GH- github issue, GH-M- github milestone, T- ticket,
NU- need-unit, TH- theme, G- gap.
"""

from __future__ import annotations

import hashlib


def stable_id(prefix: str, *parts: object, length: int = 8) -> str:
    """Content-addressed id: same inputs -> same id (reproducible evidence)."""
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return f"{prefix}{h[:length]}"


def review_id(package: str, idx: int, text: str) -> str:
    return stable_id("R-", package, idx, text[:64])


def ticket_id(idx: int, text: str) -> str:
    return stable_id("T-", idx, text[:64])


def issue_id(number: int) -> str:
    return f"GH-{number}"


def milestone_id(title: str) -> str:
    return stable_id("GH-M-", title, length=6)
