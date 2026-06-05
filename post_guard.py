import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from config import POST_GUARD_MAX_POSTS_PER_DAY, POST_GUARD_MIN_INTERVAL_MINUTES

STATE_PATH = Path(__file__).with_name("post_guard_state.json")


def _load_state():
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def can_post(channel_key: str):
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    state = _load_state()
    entry = state.get(channel_key, {"history": []})
    history = entry.get("history", [])

    parsed = []
    for item in history:
        try:
            parsed.append(datetime.fromisoformat(item))
        except Exception:
            continue

    parsed = sorted(parsed)
    recent_cutoff = now - timedelta(minutes=POST_GUARD_MIN_INTERVAL_MINUTES)
    today_count = sum(1 for ts in parsed if ts.date().isoformat() == today)
    last_ts = parsed[-1] if parsed else None

    if last_ts and last_ts >= recent_cutoff:
        return False, f"Skip: letzter erfolgreicher Post für {channel_key} war zu frisch ({last_ts.isoformat()})."

    if today_count >= POST_GUARD_MAX_POSTS_PER_DAY:
        return False, f"Skip: Tageslimit für {channel_key} bereits erreicht ({today_count}/{POST_GUARD_MAX_POSTS_PER_DAY})."

    return True, "OK"


def record_success(channel_key: str):
    now = datetime.now(timezone.utc)
    state = _load_state()
    entry = state.setdefault(channel_key, {"history": []})
    history = entry.setdefault("history", [])
    history.append(now.isoformat())

    cutoff = now - timedelta(days=7)
    trimmed = []
    for item in history:
        try:
            ts = datetime.fromisoformat(item)
        except Exception:
            continue
        if ts >= cutoff:
            trimmed.append(item)
    entry["history"] = trimmed
    _save_state(state)
