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

