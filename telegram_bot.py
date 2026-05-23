import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def send_message_to_channel(text, channel_id=None):
    """
    Sends a message to a Telegram Channel.
    If channel_id is not specified, it defaults to the configured TELEGRAM_CHANNEL_ID.
    Supports Markdown parsing and gracefully falls back to plain text if Telegram rejects formatting.
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

    # Telegram bot API endpoint
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # If text is too long, recursively send the first part, then the rest
    if len(text) > 4000:
        split_index = text.rfind('\n', 0, 4000)
        if split_index == -1:
            split_index = 4000
        first_part = text[:split_index]
        second_part = text[split_index:]
        success1 = send_message_to_channel(first_part, channel_id)
        time.sleep(1) # Wait a bit before sending the next part
        success2 = send_message_to_channel(second_part, channel_id)
        return success1 and success2
    
    payload = {
        "chat_id": target_channel,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    # Custom headers to bypass local antivirus/firewall deep packet inspection blocks
    # and prevent connection resets by looking like a standard web browser request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Connection": "close"  # Tell the server and local firewall to close connection after request, preventing socket-reuse conflicts
    }

    max_retries = 3
    retry_delay = 3  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            # Using a fresh session to isolate each network call and ensure fresh socket creation
            with requests.Session() as session:
                response = session.post(url, json=payload, headers=headers, timeout=15)
                res_json = response.json()
                
                if res_json.get("ok"):
                    print(f"Successfully posted news to Telegram Channel ({target_channel}) on attempt {attempt}!")
                    return True
                else:
                    print(f"Telegram API Error (Attempt {attempt}): {res_json.get('description')}")
                    # Try to send as plain text without Markdown if formatting fails
                    desc = res_json.get("description", "").lower()
                    if "bad request" in desc or "can't parse" in desc or "formatting" in desc:
                        print("Retrying as plain text without markdown formatting...")
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
