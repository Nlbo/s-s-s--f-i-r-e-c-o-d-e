"""Ingest app-store reviews from `sealuzh/app_reviews` (HF), filtered to one app.

The dataset is a single parquet file (~288k rows, columns: package_name, review,
date, star). We download once and cache locally (gitignored), then filter to the
target package and emit typed Signals with stable, reproducible IDs.
"""

from __future__ import annotations

import pandas as pd
import requests

from ..config import RAW_DIR
from ..ids import review_id
from ..schemas import Signal

PARQUET_URL = (
    "https://huggingface.co/api/datasets/sealuzh/app_reviews/parquet/default/train/0.parquet"
)
_CACHE = RAW_DIR / "app_reviews.parquet"


def fetch_parquet(force: bool = False) -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if force or not _CACHE.exists():
        with requests.get(PARQUET_URL, timeout=120, stream=True) as r:
            r.raise_for_status()
            with open(_CACHE, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    f.write(chunk)
    return pd.read_parquet(_CACHE)


def _parse_date(raw: object) -> str | None:
    ts = pd.to_datetime(raw, errors="coerce")
    return None if pd.isna(ts) else ts.date().isoformat()


def load_reviews(
    package: str,
    *,
    until: str | None = None,
    limit: int | None = None,
) -> list[Signal]:
    """Return reviews for `package`. `until` (ISO date) keeps only reviews on/before
    that date — used to build the T0 detection set (SPEC §2.1)."""
    df = fetch_parquet()
    df = df[df["package_name"] == package].reset_index(drop=True)

    signals: list[Signal] = []
    for idx, row in df.iterrows():
        text = str(row["review"]).strip()
        if not text:
            continue
        date = _parse_date(row.get("date"))
        if until and date and date > until:
            continue
        try:
            star = int(row["star"])
        except (TypeError, ValueError):
            star = None
        signals.append(
            Signal(
                id=review_id(package, int(idx), text),
                source="review",
                text=text,
                date=date,
                star=star,
            )
        )
        if limit and len(signals) >= limit:
            break
    return signals
