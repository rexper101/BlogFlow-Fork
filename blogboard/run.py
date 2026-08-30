import argparse
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
BACKEND_DIR = Path(__file__).parent
ROOT_DIR = BACKEND_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ── Load .env (GROQ_API_KEY etc.) ────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    env_path = BACKEND_DIR.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv is optional; export env vars manually if needed

import os
import sentry_sdk
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

# ── Import compiled graph ─────────────────────────────────────────────────────
from blogboard.graph.graph import graph


# ─────────────────────────────────────────────────────────────────────────────

def today_ist() -> str:
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(
        description="BlogBoard LangGraph Article Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  # Generate today's article (IST):
  python backend/run.py

  # Generate for a specific date:
  python backend/run.py --date 2026-03-07

  # Dry run — no LLM calls, no file writes:
  python backend/run.py --dry-run
        """,
    )
    parser.add_argument(
        "--date", type=str, default=None,
        help="Target date in YYYY-MM-DD format (default: today in IST)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview mode: skip Groq calls and file writes",
    )
    parser.add_argument(
        "--ainews", action="store_true",
        help="Run the AI News gathering and generation graph",
    )
    args = parser.parse_args()

    date_str = args.date or today_ist()
    dry_run  = args.dry_run
    run_ainews = args.ainews

 
if __name__ == "__main__":
    main()
