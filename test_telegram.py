import os
import requests
from dotenv import load_dotenv

def run_diagnostics():
    load_dotenv()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_de = os.getenv("TELEGRAM_CHANNEL_ID_DE")
    channel_en = os.getenv("TELEGRAM_CHANNEL_ID_EN")
    
    print("="*50)
    print("      NEURONEWS24 TELEGRAM DIAGNOSTICS")
    print("="*50)
    
    if not token:
        print("[X] FEHLER: Kein TELEGRAM_BOT_TOKEN in der .env gefunden!")
        return
        
    print(f"[i] Telegram Bot Token geladen: {token[:10]}...{token[-5:]}")
    
    # 1. Bot-Identität prüfen
    print("\n--- Schritt 1: Bot-Identität prüfen ---")
    get_me_url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        res = requests.get(get_me_url, timeout=10)
        data = res.json()
        if data.get("ok"):
            bot_username = data["result"]["username"]
            bot_first_name = data["result"]["first_name"]
            print(f"[OK] Bot erfolgreich verbunden!")
            print(f"     -> Name: {bot_first_name}")
            print(f"     -> Username: @{bot_username}")
            print(f"     -> WICHTIG: Suchen Sie in Telegram genau nach @{bot_username}")
            print(f"        und stellen Sie sicher, dass exakt DIESER Bot in Ihren Kanälen Admin ist!")
        else:
            print(f"[X] FEHLER: Der Token ist ungültig! Telegram sagt: {data.get('description')}")
            return
    except Exception as e:
        print(f"[X] Verbindung fehlgeschlagen: {e}")
        return

    # 2. Kanäle prüfen
    for lang, channel_id in [("Deutsch", channel_de), ("Englisch", channel_en)]:
        print(f"\n--- Schritt 2: {lang}-Kanal prüfen ({channel_id}) ---")
        if not channel_id:
            print(f"[X] Kein Kanal für {lang} in der .env konfiguriert.")
            continue
            
        # Versuchen, Chat-Informationen abzurufen
        get_chat_url = f"https://api.telegram.org/bot{token}/getChat?chat_id={channel_id}"
        try:
            res = requests.get(get_chat_url, timeout=10)
            data = res.json()
            if data.get("ok"):
                chat_title = data["result"].get("title")
                chat_type = data["result"].get("type")
                print(f"[OK] Kanal gefunden!")
                print(f"     -> Titel: {chat_title}")
                print(f"     -> Typ: {chat_type}")
                
                # Prüfen, ob Bot Admin ist
                get_member_url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id={channel_id}&user_id={data['result'].get('id') or 8863984063}"
                # Let's check the bot's own membership status
                get_admins_url = f"https://api.telegram.org/bot{token}/getChatAdministrators?chat_id={channel_id}"
                admin_res = requests.get(get_admins_url, timeout=10)
                admin_data = admin_res.json()
                
                if admin_data.get("ok"):
                    # Find if our bot is in the admin list
                    admins = admin_data["result"]
                    is_admin = False
                    for admin in admins:
                        if admin["user"]["username"].lower() == bot_username.lower():
                            is_admin = True
                            print(f"[OK] Der Bot @{bot_username} ist als Administrator im Kanal eingetragen!")
                            break
                    if not is_admin:
                        print(f"[X] FEHLER: Der Bot @{bot_username} ist NICHT als Administrator im Kanal eingetragen!")
                        print(f"    Bitte fügen Sie @{bot_username} als Admin hinzu.")
                else:
                    print(f"[X] FEHLER: Keine Admin-Liste abrufbar. Telegram sagt: {admin_data.get('description')}")
            else:
                desc = data.get("description", "")
                print(f"[X] FEHLER: Zugriff verweigert oder Kanal nicht gefunden.")
                print(f"    Telegram sagt: '{desc}'")
                
                if "forbidden" in desc.lower() or "member" in desc.lower():
                    print("\n    Mögliche Ursachen & Lösungen:")
                    print(f"    1. Sie haben den falschen Bot zum Kanal hinzugefügt.")
                    print(f"       Suchen Sie in Telegram nach @{bot_username} und fügen Sie ihn hinzu.")
                    print(f"    2. Ihr Kanal ist eventuell doch PRIVAT und nicht ÖFFENTLICH.")
                    print(f"       Gehen Sie in die Kanaleinstellungen -> Kanaltyp -> Stellen Sie ihn auf 'Öffentlich'")
                    print(f"       und weisen Sie ihm den Link-Namen '{channel_id.replace('@', '')}' zu.")
        except Exception as e:
            print(f"[X] Verbindung fehlgeschlagen beim Prüfen von {channel_id}: {e}")

    print("\n" + "="*50)
    print("             DIAGNOSE BEENDET")
    print("="*50)

if __name__ == "__main__":
    run_diagnostics()
