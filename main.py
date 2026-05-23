import sys
from fetcher import fetch_recent_news
from summarizer import summarize_articles
from telegram_bot import send_message_to_channel
from config import BOT_MODE, TELEGRAM_CHANNEL_ID, TELEGRAM_CHANNEL_ID_DE, TELEGRAM_CHANNEL_ID_EN


def print_result(mode_name, success):
    if success:
        print(f"=== {mode_name.upper()} RUN COMPLETED SUCCESSFULLY ===")
    else:
        print(f"=== {mode_name.upper()} RUN FAILED ===")


def run_pipeline() -> int:
    print("=== STARTING DAILY AI NEWS TELEGRAM BOT ===")
    print(f"Current BOT_MODE: {BOT_MODE.upper()}")

    articles = fetch_recent_news(hours=24)
    if not articles:
        print("No articles found in the last 24 hours. Nothing to post.")
        return 1

    overall_success = True

    if BOT_MODE in ("german_only", "deutsch_only"):
        print("Processing German news...")
        digest_de = summarize_articles(articles, language="German")
        success = False
        if digest_de:
            success = send_message_to_channel(digest_de, channel_id=TELEGRAM_CHANNEL_ID_DE)
        else:
            print("Failed to generate German digest.")
        print_result("German Only", success)
        overall_success = overall_success and success

    elif BOT_MODE == "english_only":
        print("Processing English news...")
        digest_en = summarize_articles(articles, language="English")
        success = False
        if digest_en:
            success = send_message_to_channel(digest_en, channel_id=TELEGRAM_CHANNEL_ID_EN)
        else:
            print("Failed to generate English digest.")
        print_result("English Only", success)
        overall_success = overall_success and success

    elif BOT_MODE == "bilingual_single_channel":
        print("Processing bilingual news for a single channel...")

        print("Generating German digest...")
        digest_de = summarize_articles(articles, language="German")
        print("Generating English digest...")
        digest_en = summarize_articles(articles, language="English")

        success_de = False
        success_en = False

        if digest_de:
            print("Posting German digest...")
            success_de = send_message_to_channel(digest_de, channel_id=TELEGRAM_CHANNEL_ID)
        else:
            print("Failed to generate German digest.")

        if digest_en:
            print("Posting English digest...")
            success_en = send_message_to_channel(digest_en, channel_id=TELEGRAM_CHANNEL_ID)
        else:
            print("Failed to generate English digest.")

        print_result("Bilingual Single Channel (German)", success_de)
        print_result("Bilingual Single Channel (English)", success_en)
        overall_success = overall_success and success_de and success_en

    elif BOT_MODE == "two_channels":
        print("Processing bilingual news for two separate channels...")

        print("Generating German digest...")
        digest_de = summarize_articles(articles, language="German")
        success_de = False
        if digest_de:
            print(f"Posting to German Channel: {TELEGRAM_CHANNEL_ID_DE}")
            success_de = send_message_to_channel(digest_de, channel_id=TELEGRAM_CHANNEL_ID_DE)
        else:
            print("Failed to generate German digest.")

        print("Generating English digest...")
        digest_en = summarize_articles(articles, language="English")
        success_en = False
        if digest_en:
            print(f"Posting to English Channel: {TELEGRAM_CHANNEL_ID_EN}")
            success_en = send_message_to_channel(digest_en, channel_id=TELEGRAM_CHANNEL_ID_EN)
        else:
            print("Failed to generate English digest.")

        print_result("Two Channels (German Channel)", success_de)
        print_result("Two Channels (English Channel)", success_en)
        overall_success = overall_success and success_de and success_en

    else:
        print(f"Unknown BOT_MODE '{BOT_MODE}'.")
        return 1

    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
