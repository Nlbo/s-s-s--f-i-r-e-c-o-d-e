"""Web control panel (FastAPI): pick the model + target product, run the pipeline
from the browser with live progress, and view the Ant-Design report — for a live,
retargetable demo. Launch with `sss serve`.

The pipeline runs in a background thread; the UI polls /api/status. Only one run at a
time. Keys still come from the environment / .env — the panel never handles secrets.
"""

from __future__ import annotations

import dataclasses
import json
import threading
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from .config import OUT_DIR, get_settings
from .pipeline import run as run_pipeline

TEMPLATES = Path(__file__).parent / "templates"

PRESETS = [
    {"name": "WordPress (tuned)", "pkg": "org.wordpress.android",
     "repo": "wordpress-mobile/WordPress-Android"},
    {"name": "AntennaPod", "pkg": "de.danoeh.antennapod", "repo": "AntennaPod/AntennaPod"},
    {"name": "Telegram", "pkg": "org.telegram.messenger", "repo": "DrKLO/Telegram"},
    {"name": "Wikipedia", "pkg": "org.wikipedia", "repo": "wikimedia/apps-android-wikipedia"},
]

# single-run status shared with the UI
_status: dict = {"running": False, "stage": "idle", "frac": 0.0, "error": None, "done": False}
_lock = threading.Lock()


class RunReq(BaseModel):
    model: str = "gpt-5.1"          # "offline" | "gpt-4.1-mini" | "gpt-5.1"
    app_package: str = "org.wordpress.android"
    github_repo: str = "wordpress-mobile/WordPress-Android"
    t0: str = "2017-01-01"
    max_signals: int = 4000


def _do_run(req: RunReq) -> None:
    offline = req.model == "offline"
    base = get_settings()
    settings = dataclasses.replace(
        base,
        target_app_package=req.app_package.strip(),
        target_github_repo=req.github_repo.strip(),
        analysis_t0=req.t0.strip(),
        openai_model=(base.openai_model if offline else req.model),
        max_signals=int(req.max_signals),
    )

    def on_stage(label: str, frac: float) -> None:
        with _lock:
            _status.update(stage=label, frac=round(frac, 3))

    try:
        run_pipeline(settings, offline=offline, on_stage=on_stage)
        with _lock:
            _status.update(running=False, done=True, stage="Done", frac=1.0, error=None)
    except Exception as e:  # noqa: BLE001 - surface any failure to the UI, don't crash the server
        name = type(e).__name__
        msg = str(e).strip() or name
        if any(k in name for k in ("RetryError", "Connection", "RateLimit", "Timeout")):
            msg = ("the model API kept failing (rate limit or connection). Try again, "
                   "lower Max signals, or pick the offline model.")
        with _lock:
            _status.update(running=False, done=True, stage="Failed", error=msg[:300])


def create_app() -> FastAPI:
    app = FastAPI(title="The Silent Stakeholder")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return (TEMPLATES / "control_panel.html").read_text()

    @app.get("/api/config")
    def config() -> JSONResponse:
        s = get_settings()
        return JSONResponse({
            "presets": PRESETS,
            "backend": s.backend,
            "has_github_token": bool(s.github_token),
            "models": ["gpt-5.1", "gpt-4.1-mini", "offline"],
            "defaults": {"t0": s.analysis_t0, "max_signals": 4000},
        })

    @app.post("/api/run")
    def start(req: RunReq) -> JSONResponse:
        with _lock:
            if _status["running"]:
                return JSONResponse({"ok": False, "error": "a run is already in progress"}, 409)
            _status.update(running=True, done=False, stage="Queued…", frac=0.0, error=None,
                           started=time.time())
        threading.Thread(target=_do_run, args=(req,), daemon=True).start()
        return JSONResponse({"ok": True})

    @app.get("/api/status")
    def status() -> JSONResponse:
        with _lock:
            out = dict(_status)
        rp = OUT_DIR / "report.json"
        if out.get("done") and not out.get("error") and rp.exists():
            d = json.loads(rp.read_text())
            out["report"] = {
                "one_sentence_gap": d.get("one_sentence_gap"),
                "meta": d.get("meta"),
                "gaps": [
                    {"rank": g["rank"], "need": g["need"], "verdict": g["verdict"],
                     "confidence": g["confidence"],
                     "backtest": (g.get("validation") or {}).get("note", "")}
                    for g in d.get("gaps", [])
                ],
            }
        return JSONResponse(out)

    @app.get("/report.html", response_class=HTMLResponse)
    def report_html() -> str:
        p = OUT_DIR / "report.html"
        return p.read_text() if p.exists() else "<p>No report yet — run an analysis.</p>"

    return app


app = create_app()
