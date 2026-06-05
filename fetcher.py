import feedparser
import time
import re
from datetime import datetime, timedelta, timezone
from config import RSS_FEEDS


def fetch_recent_news(hours=24):
    """
    Fetches news from RSS feeds and returns only items from the last N hours.
    If no live items are found, returns an empty list (no fake/mock news).
    """
    articles = []
    now = datetime.now(timezone.utc)
    time_limit = now - timedelta(hours=hours)

    print(f"Fetching articles from the last {hours} hours...")

    for feed_url in RSS_FEEDS:
        try:
            print(f"Parsing feed: {feed_url}")
            feed = feedparser.parse(feed_url)

            status = feed.get("status")
            if status == 403:
                print(f"Warning: Access to {feed_url} was blocked (HTTP 403 Forbidden).")
                continue

            for entry in feed.entries:
                published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")

                if published_parsed:
                    published_dt = datetime.fromtimestamp(time.mktime(published_parsed), timezone.utc)
                else:
                    published_dt = now

                if published_dt >= time_limit:
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "").strip()
                    summary = (entry.get("summary", "") or entry.get("description", "")).strip()

                    clean_summary = re.sub(r"<[^>]+>", "", summary).strip()
                    if len(clean_summary) > 500:
                        clean_summary = clean_summary[:500] + "..."

                    articles.append(
                        {
                            "title": title,
                            "link": link,
                            "summary": clean_summary,
                            "source": feed.feed.get("title", feed_url),
                            "published": published_dt.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {e}")

    # Remove duplicates by link (or title if link is missing)
    unique_articles = []
    seen_keys = set()

    for art in articles:
        key = art["link"] if art["link"] else art["title"]
        if key and key not in seen_keys:
            seen_keys.add(key)
            unique_articles.append(art)

    if not unique_articles:
        print("\n[INFO] No live feed items found. Skipping post for this run.")
        return []

    print(f"Fetched {len(unique_articles)} articles.")
    return unique_articles


if __name__ == "__main__":
    # Test fetcher
    articles = fetch_recent_news(24)
    for idx, art in enumerate(articles[:3]):
        print(f"\n[{idx + 1}] {art['title']}")
        print(f"Source: {art['source']}")
        print(f"Link: {art['link']}")
