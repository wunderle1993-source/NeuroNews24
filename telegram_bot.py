import os
import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


def send_message_to_channel(text, channel_id=None):
    """
    Sends a message to a Telegram Channel.
    If channel_id is not specified, it defaults to the configured TELEGRAM_CHANNEL_ID.
    Supports HTML parsing and gracefully falls back to plain text if Telegram rejects formatting.
    Includes a robust retry mechanism with custom headers to prevent ConnectionResetError (10054).
    """
    target_channel = channel_id or TELEGRAM_CHANNEL_ID

    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not configured in .env!")
        return False

    if not target_channel:
        print("Error: Target Telegram Channel ID is not specified or configured!")
        return False

    print(f"Sending message to channel: {target_channel}...")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    if len(text) > 4000:
        split_index = text.rfind("\n", 0, 4000)
        if split_index == -1:
            split_index = 4000
        first_part = text[:split_index]
        second_part = text[split_index:]
        success1 = send_message_to_channel(first_part, channel_id)
        time.sleep(1)
        success2 = send_message_to_channel(second_part, channel_id)
        return success1 and success2

    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    payload = {
        "chat_id": target_channel,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Connection": "close",
    }

    max_retries = 3
    retry_delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            with requests.Session() as session:
                response = session.post(url, json=payload, headers=headers, timeout=15)
                res_json = response.json()

                if res_json.get("ok"):
                    print(f"Successfully posted news to Telegram Channel ({target_channel}) on attempt {attempt}!")
                    return True

                print(f"Telegram API Error (Attempt {attempt}): {res_json.get('description')}")
                desc = res_json.get("description", "").lower()
                if "bad request" in desc or "can't parse" in desc or "formatting" in desc:
                    print("Retrying as plain text without HTML formatting...")
                    payload.pop("parse_mode", None)
                    retry_response = session.post(url, json=payload, headers=headers, timeout=15)
                    if retry_response.json().get("ok"):
                        print(f"Successfully posted news (plain text fallback) to {target_channel}!")
                        return True
                return False

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Network error on attempt {attempt}/{max_retries} for channel {target_channel}: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds with a completely fresh network connection...")
                time.sleep(retry_delay)
            else:
                print(f"All {max_retries} attempts failed due to network-level errors.")
                return False
        except Exception as e:
            print(f"Unexpected error in send_message_to_channel on attempt {attempt}: {e}")
            return False

    return False


def send_photo_from_url(photo_url: str, caption: str = "", channel_id=None) -> bool:
    target_channel = channel_id or TELEGRAM_CHANNEL_ID
    if not TELEGRAM_BOT_TOKEN or not target_channel or not photo_url:
        return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Connection": "close",
    }

    try:
        with requests.Session() as session:
            image_response = session.get(photo_url, headers=headers, timeout=20)
            image_response.raise_for_status()
            content_type = image_response.headers.get("Content-Type", "image/jpeg")
            extension = ".jpg"
            if "png" in content_type:
                extension = ".png"
            elif "webp" in content_type:
                extension = ".webp"

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            data = {
                "chat_id": target_channel,
                "caption": (caption or "")[:1024],
                "parse_mode": "HTML",
                "show_caption_above_media": True,
            }
            files = {
                "photo": (f"hero{extension}", image_response.content, content_type),
            }
            response = session.post(url, data=data, files=files, headers={"User-Agent": headers["User-Agent"]}, timeout=30)
            res_json = response.json()
            if res_json.get("ok"):
                print(f"Hero image sent to {target_channel}.")
                return True
            print(f"Hero image skipped: {res_json.get('description')}")
            return False
    except Exception as exc:
        print(f"Hero image download/upload skipped: {exc}")
        return False
