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
    # Underground / Reddit
    "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",
    "https://www.reddit.com/r/singularity/top/.rss?t=day",
    "https://www.reddit.com/r/artificial/top/.rss?t=day",
    "https://www.reddit.com/r/MachineLearning/top/.rss?t=day",
    "https://www.reddit.com/r/AIJailbreak/top/.rss?t=day",

    # Security & Exploits
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews",

    # AI News
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://hackaday.com/category/artificial-intelligence/feed/",

    # Research
    "https://export.arxiv.org/rss/cs.AI",
    "https://export.arxiv.org/rss/cs.CR",

    # German AI
    "https://www.heise.de/rss/heise-atom.xml",
    "https://www.golem.de/rss.php?tp=ki",
]
