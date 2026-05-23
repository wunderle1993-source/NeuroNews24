import os
from dotenv import load_dotenv

load_dotenv()


def _env(name, default=None):
    value = os.getenv(name)
    if value is None:
        return default
    cleaned = value.strip()
    return cleaned or default


TELEGRAM_BOT_TOKEN = _env("TELEGRAM_BOT_TOKEN")

TELEGRAM_CHANNEL_ID = _env("TELEGRAM_CHANNEL_ID")

TELEGRAM_CHANNEL_ID_DE = _env("TELEGRAM_CHANNEL_ID_DE", TELEGRAM_CHANNEL_ID)
TELEGRAM_CHANNEL_ID_EN = _env("TELEGRAM_CHANNEL_ID_EN", TELEGRAM_CHANNEL_ID)

GEMINI_API_KEY = _env("GEMINI_API_KEY")

BOT_MODE = _env("BOT_MODE", "german_only").lower()

RSS_FEEDS = [
    "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",
    "https://www.reddit.com/r/singularity/top/.rss?t=day",
    "https://www.bleepingcomputer.com/feed/",
    "https://hackaday.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]
