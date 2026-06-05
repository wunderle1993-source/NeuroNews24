import os
from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "").strip()
TELEGRAM_CHANNEL_ID_DE = (os.getenv("TELEGRAM_CHANNEL_ID_DE", "").strip() or TELEGRAM_CHANNEL_ID)
TELEGRAM_CHANNEL_ID_EN = (os.getenv("TELEGRAM_CHANNEL_ID_EN", "").strip() or TELEGRAM_CHANNEL_ID)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_FALLBACK_KEY = os.getenv("GROQ_FALLBACK_KEY", "").strip()

BOT_MODE = os.getenv("BOT_MODE", "german_only").strip().lower()
POST_GUARD_MIN_INTERVAL_MINUTES = 360
POST_GUARD_MAX_POSTS_PER_DAY = 2

RSS_FEEDS = [
    "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",
    "https://www.reddit.com/r/singularity/top/.rss?t=day",
    "https://www.bleepingcomputer.com/feed/",
    "https://hackaday.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
]


def _looks_like_channel(value: str) -> bool:
    return bool(value) and (value.startswith("@") or value.startswith("-100"))


def validate_runtime_config():
    errors = []
    warnings = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN fehlt.")

    valid_modes = {
        "german_only",
        "deutsch_only",
        "english_only",
        "bilingual_single_channel",
        "two_channels",
    }
    if BOT_MODE not in valid_modes:
        errors.append(f"BOT_MODE '{BOT_MODE}' ist ungueltig.")

    if BOT_MODE in {"german_only", "deutsch_only"} and not _looks_like_channel(TELEGRAM_CHANNEL_ID_DE):
        errors.append("TELEGRAM_CHANNEL_ID_DE fehlt oder ist ungueltig.")

    if BOT_MODE == "english_only" and not _looks_like_channel(TELEGRAM_CHANNEL_ID_EN):
        errors.append("TELEGRAM_CHANNEL_ID_EN fehlt oder ist ungueltig.")

    if BOT_MODE == "bilingual_single_channel" and not _looks_like_channel(TELEGRAM_CHANNEL_ID):
        errors.append("TELEGRAM_CHANNEL_ID fehlt oder ist ungueltig.")

    if BOT_MODE == "two_channels":
        if not _looks_like_channel(TELEGRAM_CHANNEL_ID_DE):
            errors.append("TELEGRAM_CHANNEL_ID_DE fehlt oder ist ungueltig.")
        if not _looks_like_channel(TELEGRAM_CHANNEL_ID_EN):
            errors.append("TELEGRAM_CHANNEL_ID_EN fehlt oder ist ungueltig.")

    if not any([GROQ_API_KEY, GROQ_FALLBACK_KEY]):
        errors.append("Kein LLM-Key konfiguriert. Erwartet: GROQ_API_KEY oder GROQ_FALLBACK_KEY.")

    if GROQ_API_KEY and not GROQ_API_KEY.startswith("gsk_"):
        errors.append("GROQ_API_KEY hat kein Groq-Praefix 'gsk_'.")
    if GROQ_FALLBACK_KEY and not GROQ_FALLBACK_KEY.startswith("gsk_"):
        errors.append("GROQ_FALLBACK_KEY hat kein Groq-Praefix 'gsk_'.")

    if GROQ_API_KEY.startswith("AIza") or GROQ_FALLBACK_KEY.startswith("AIza"):
        errors.append("Ein Google-Key steckt in einem Groq-Feld. Key-Felder sind vertauscht.")

    if not GROQ_API_KEY and GROQ_FALLBACK_KEY:
        warnings.append("Nur GROQ_FALLBACK_KEY gesetzt. Besser auch GROQ_API_KEY pflegen.")

    return errors, warnings
