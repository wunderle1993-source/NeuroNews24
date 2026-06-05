import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOCK_PATH = Path(__file__).with_name("run.lock")
STALE_AFTER_MINUTES = 120


def acquire_lock():
    now = datetime.now(timezone.utc)
    if LOCK_PATH.exists():
        try:
            data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
            started_at = datetime.fromisoformat(data.get("started_at", ""))
        except Exception:
            started_at = None

        if started_at and started_at >= now - timedelta(minutes=STALE_AFTER_MINUTES):
            return False, f"Skip: anderer Run ist noch aktiv seit {started_at.isoformat()}."

    LOCK_PATH.write_text(
        json.dumps({"pid": os.getpid(), "started_at": now.isoformat()}, indent=2),
        encoding="utf-8",
    )
    return True, "Run-Lock gesetzt."


def release_lock():
    try:
        LOCK_PATH.unlink(missing_ok=True)
    except Exception:
        pass
