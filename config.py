import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Default or legacy channel ID
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Language-specific channel IDs (fall back to the default channel ID if not set)
TELEGRAM_CHANNEL_ID_DE = os.getenv("TELEGRAM_CHANNEL_ID_DE") or TELEGRAM_CHANNEL_ID
TELEGRAM_CHANNEL_ID_EN = os.getenv("TELEGRAM_CHANNEL_ID_EN") or TELEGRAM_CHANNEL_ID

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# BOT_MODE can be:
# - 'german_only' : Send German news to TELEGRAM_CHANNEL_ID_DE (or TELEGRAM_CHANNEL_ID)
# - 'english_only': Send English news to TELEGRAM_CHANNEL_ID_EN (or TELEGRAM_CHANNEL_ID)
# - 'bilingual_single_channel': Send both German and English news to TELEGRAM_CHANNEL_ID (as two messages)
# - 'two_channels': Send German news to TELEGRAM_CHANNEL_ID_DE and English news to TELEGRAM_CHANNEL_ID_EN
BOT_MODE = os.getenv("BOT_MODE", "german_only").lower()

# List of AI RSS feeds to pull news from
# Updated to focus on leaks, jailbreaks, open-source AI models, and hacking
RSS_FEEDS = [
    "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",
    "https://www.reddit.com/r/singularity/top/.rss?t=day",
    "https://www.bleepingcomputer.com/feed/",
    "https://hackaday.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]
