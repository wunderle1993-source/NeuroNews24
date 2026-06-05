import sys
from fetcher import fetch_recent_news
from post_guard import can_post, record_success
from run_lock import acquire_lock, release_lock
from summarizer import summarize_articles
from telegram_bot import send_message_to_channel
from config import (
    BOT_MODE,
    TELEGRAM_CHANNEL_ID,
    TELEGRAM_CHANNEL_ID_DE,
    TELEGRAM_CHANNEL_ID_EN,
    validate_runtime_config,
)


def post_with_guard(text, channel_id, force_post=False):
    if force_post:
        success = send_message_to_channel(text, channel_id=channel_id)
        if success:
            record_success(channel_id)
        return success

    allowed, reason = can_post(channel_id)
    print(f"[POST GUARD] {reason}")
    if not allowed:
        return True

    success = send_message_to_channel(text, channel_id=channel_id)
    if success:
        record_success(channel_id)
    return success


def run_pipeline(force_post=False):
    print("=== STARTING DAILY AI NEWS TELEGRAM BOT ===")
    print(f"Current BOT_MODE: {BOT_MODE.upper()}")

    errors, warnings = validate_runtime_config()
    for warning in warnings:
        print(f"[CONFIG WARNING] {warning}")
    if errors:
        for error in errors:
            print(f"[CONFIG ERROR] {error}")
        sys.exit(1)

    lock_acquired, lock_reason = acquire_lock()
    print(f"[RUN LOCK] {lock_reason}")
    if not lock_acquired:
        sys.exit(0)

    try:
        de_allowed, de_reason = True, "force mode"
        en_allowed, en_reason = True, "force mode"

        if not force_post:
            if BOT_MODE in {"german_only", "deutsch_only", "two_channels"}:
                de_allowed, de_reason = can_post(TELEGRAM_CHANNEL_ID_DE)
                print(f"[POST GUARD] {de_reason}")
            if BOT_MODE in {"english_only", "two_channels"}:
                en_allowed, en_reason = can_post(TELEGRAM_CHANNEL_ID_EN)
                print(f"[POST GUARD] {en_reason}")
            if BOT_MODE == "bilingual_single_channel":
                de_allowed, de_reason = can_post(TELEGRAM_CHANNEL_ID)
                print(f"[POST GUARD] {de_reason}")
                en_allowed = de_allowed

        if BOT_MODE in {"german_only", "deutsch_only"} and not de_allowed:
            print_result("German Only", True)
            return
        if BOT_MODE == "english_only" and not en_allowed:
            print_result("English Only", True)
            return
        if BOT_MODE == "bilingual_single_channel" and not de_allowed and not en_allowed:
            print_result("Bilingual Single Channel", True)
            return
        if BOT_MODE == "two_channels" and not de_allowed and not en_allowed:
            print_result("Two Channels", True)
            return

        articles = fetch_recent_news(hours=24)
        if not articles:
            print("No articles found in the last 24 hours. Nothing to post.")
            sys.exit(0)

        if BOT_MODE == "german_only" or BOT_MODE == "deutsch_only":
            print("Processing German news...")
            digest_de = summarize_articles(articles, language="German")
            if digest_de:
                success = post_with_guard(digest_de, TELEGRAM_CHANNEL_ID_DE, force_post=force_post)
                print_result("German Only", success)
            else:
                print("Failed to generate German digest.")

        elif BOT_MODE == "english_only":
            print("Processing English news...")
            digest_en = summarize_articles(articles, language="English")
            if digest_en:
                success = post_with_guard(digest_en, TELEGRAM_CHANNEL_ID_EN, force_post=force_post)
                print_result("English Only", success)
            else:
                print("Failed to generate English digest.")

        elif BOT_MODE == "bilingual_single_channel":
            print("Processing bilingual news for a single channel...")
            print("Generating German digest...")
            digest_de = summarize_articles(articles, language="German")
            print("Generating English digest...")
            digest_en = summarize_articles(articles, language="English")

            success_de, success_en = False, False

            if digest_de:
                print("Posting German digest...")
                success_de = post_with_guard(digest_de, TELEGRAM_CHANNEL_ID, force_post=force_post)
            else:
                print("Failed to generate German digest.")

            if digest_en:
                print("Posting English digest...")
                success_en = post_with_guard(digest_en, TELEGRAM_CHANNEL_ID, force_post=force_post)
            else:
                print("Failed to generate English digest.")

            print_result("Bilingual Single Channel (German)", success_de)
            print_result("Bilingual Single Channel (English)", success_en)

        elif BOT_MODE == "two_channels":
            print("Processing bilingual news for two separate channels...")

            success_de = False
            if de_allowed:
                print("Generating German digest...")
                digest_de = summarize_articles(articles, language="German")
                if digest_de:
                    print(f"Posting to German Channel: {TELEGRAM_CHANNEL_ID_DE}")
                    success_de = post_with_guard(digest_de, TELEGRAM_CHANNEL_ID_DE, force_post=force_post)
                else:
                    print("Failed to generate German digest.")
            else:
                success_de = True

            success_en = False
            if en_allowed:
                print("Generating English digest...")
                digest_en = summarize_articles(articles, language="English")
                if digest_en:
                    print(f"Posting to English Channel: {TELEGRAM_CHANNEL_ID_EN}")
                    success_en = post_with_guard(digest_en, TELEGRAM_CHANNEL_ID_EN, force_post=force_post)
                else:
                    print("Failed to generate English digest.")
            else:
                success_en = True

            print_result("Two Channels (German Channel)", success_de)
            print_result("Two Channels (English Channel)", success_en)

        else:
            print(f"Unknown BOT_MODE '{BOT_MODE}'. Defaulting to German only.")
            digest_de = summarize_articles(articles, language="German")
            if digest_de:
                success = post_with_guard(digest_de, TELEGRAM_CHANNEL_ID_DE, force_post=force_post)
                print_result("Default German", success)
    finally:
        release_lock()


def print_result(mode_name, success):
    if success:
        print(f"=== {mode_name.upper()} RUN COMPLETED SUCCESSFULLY ===")
    else:
        print(f"=== {mode_name.upper()} RUN FAILED ===")


if __name__ == "__main__":
    force_post = "--force" in sys.argv
    run_pipeline(force_post=force_post)
