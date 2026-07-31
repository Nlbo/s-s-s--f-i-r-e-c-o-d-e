"""Hermetic fixtures — synthetic signals/roadmap so tests run fast with no network."""

from __future__ import annotations

import pytest

from silent_stakeholder.schemas import RoadmapItem, Signal


def _rev(i: int, text: str, star: int) -> Signal:
    return Signal(id=f"R-test{i:03d}", source="review", text=text, star=star, date="2016-09-01")


# (text, star) grouped by intended theme
_LOGIN = [
    "Cannot log in to my self hosted site, keeps saying error",
    "Login problem, not able to sign in to my own website anymore",
    "Won't connect to my self-hosted WordPress, authentication fails every time",
    "Keeps logging me out, have to sign in again and again",
    "Sign in broken after update, cannot access my blog",
    "Login failed repeatedly on my self hosted install",
]
_UPLOAD = [
    "Image upload fails constantly, photos never attach to my post",
    "Cannot upload pictures, media upload always errors out",
    "Uploading images does not work, upload gets stuck forever",
    "Photo upload broken, my media never uploads",
    "Media upload keeps failing when I add images to a post",
]
_EDITOR = [
    "The editor lost my draft, I lost my whole blog post",
    "Writing disappears, draft not saved, lost everything I wrote",
    "Editor is a mess, my post got deleted before publishing",
    "Lost my draft again, the editor did not save my work",
    "My unsaved post vanished, the editor keeps losing text",
]
_PRAISE = [
    "Great app, love blogging on the go",
    "Very nice and easy to use, works well",
    "Good app for managing my website, happy with it",
    "Awesome, does what I need",
    "Nice and simple, recommend it",
]


@pytest.fixture
def signals() -> list[Signal]:
    groups = [(_LOGIN, 1), (_UPLOAD, 2), (_EDITOR, 1), (_PRAISE, 5)]
    rows = [(text, star) for texts, star in groups for text in texts]
    return [_rev(i, text, star) for i, (text, star) in enumerate(rows)]


@pytest.fixture
def roadmap() -> list[RoadmapItem]:
    return [
        RoadmapItem(
            id="GH-1001", kind="issue",
            title="Fix image upload crash on large files",
            body="Uploading very large images crashes the media picker.",
            labels=["[Type] Bug"], priority=None, state="open", created_at="2016-05-01",
        ),
        RoadmapItem(
            id="GH-M-rel", kind="milestone", title="5.0",
            body="Reader improvements and notification revamp.",
            state="open", created_at="2016-08-01",
        ),
    ]
