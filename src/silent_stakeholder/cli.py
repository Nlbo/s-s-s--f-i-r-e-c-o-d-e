"""Command-line entrypoint: `sss <command>`.

Subcommands are wired to pipeline stages as they come online (SPEC §12).
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .config import ensure_dirs, get_settings


def _cmd_version(_args: argparse.Namespace) -> int:
    print(f"silent-stakeholder {__version__}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    from .pipeline import run

    ensure_dirs()
    settings = get_settings()
    run(settings, limit=args.limit, offline=args.offline)
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    ensure_dirs()
    print(f"Control panel  ->  http://{args.host}:{args.port}")
    uvicorn.run("silent_stakeholder.web:app", host=args.host, port=args.port, log_level="warning")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sss", description="The Silent Stakeholder pipeline.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="print version").set_defaults(func=_cmd_version)

    run_p = sub.add_parser("run", help="run the full pipeline -> out/report.*")
    run_p.add_argument("--limit", type=int, default=None, help="cap number of signals (debug)")
    run_p.add_argument(
        "--offline",
        action="store_true",
        help="deterministic local models (no LLM calls); uses cached datasets, a shallow "
        "roadmap, and skips the token-based backtest",
    )
    run_p.set_defaults(func=_cmd_run)

    serve_p = sub.add_parser("serve", help="launch the web control panel")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8000)
    serve_p.set_defaults(func=_cmd_serve)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
