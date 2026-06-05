# 🤖 Automatisierter Telegram-Kanal für tägliche KI-News (Mehrsprachig)

Dieses Projekt ermöglicht es Ihnen, vollautomatisch einen oder mehrere Telegram-Kanäle zu betreiben, die jeden Tag die neuesten KI-Nachrichten sammeln, mithilfe von Googles **Gemini-Modell** auf Deutsch und/oder Englisch zusammenfassen und an Ihre Kanäle posten.

Wir haben das Projekt direkt in Ihrer Sandbox-Umgebung erweitert! Sie haben nun die **absolute Freiheit**, wie Sie Ihre News veröffentlichen möchten:
1. **Nur auf Deutsch** (in einen deutschen Kanal).
2. **Nur auf Englisch** (in einen englischen Kanal).
3. **Zweisprachig in einem einzigen Kanal** (zuerst der deutsche Post, direkt danach der englische Post).
4. **Aufgeteilt auf zwei Kanäle** (ein Kanal für deutsche Leser, ein Kanal für englische Leser – vollautomatisch gesteuert durch dasselbe Skript!).

---\n\n## 📂 Dateistruktur in Ihrem Workspace

Die folgenden Dateien wurden für Sie aktualisiert bzw. erstellt:
1. **[`requirements.txt`](file:///telegram_ai_news_bot/requirements.txt)**: Enthält die Python-Bibliotheken (`feedparser`, `requests`, `google-generativeai`, `python-dotenv`).
2. **[`.env.example`](file:///telegram_ai_news_bot/.env.example)**: Vorlage für Ihre API-Keys, Betriebsmodi und Kanäle.
3. **[`config.py`](file:///telegram_ai_news_bot/config.py)**: Verwaltet die Konfigurationen, liest die neuen Umgebungsvariablen aus und enthält die RSS-Feeds (z. B. OpenAI Blog, TechCrunch AI, VentureBeat, arXiv).
4. **[`fetcher.py`](file:///telegram_ai_news_bot/fetcher.py)**: Holt die neuesten Artikel der letzten 24 Stunden über RSS-Feeds ein.
5. **[`summarizer.py`](file:///telegram_ai_news_bot/summarizer.py)**: Sendet die Artikel an Gemini und lässt sie dynamisch nach Sprachauswahl (Deutsch/Englisch) filtern und im Telegram-Format zusammenfassen.
6. **[`telegram_bot.py`](file:///telegram_ai_news_bot/telegram_bot.py)**: Postet das fertige Digest flexibel an die jeweils dafür vorgesehene Kanal-ID.
7. **[`main.py`](file:///telegram_ai_news_bot/main.py)**: Das Hauptskript, das je nach eingestelltem Modus die Feeds zieht, die KI-Zusammenfassungen generiert und sie an die korrekten Kanäle sendet.

---\n\n## 🛠️ Einrichtung & Konfiguration

### Schritt 1: Telegram Bot & Kanäle erstellen
1. Suchen Sie in Telegram nach **@BotFather** und senden Sie `/newbot`. Folgen Sie den Anweisungen, um einen Namen und Benutzernamen festzulegen. Kopieren Sie den **HTTP API Token** (z. B. `123456789:ABCdefGhIJKlmNoPQRsTuvWxYz`).
2. Erstellen Sie die gewünschten Telegram-Kanäle (einen für Deutsch, einen für Englisch oder einfach einen gemeinsamen Kanal, je nach Wunsch).
3. Fügen Sie Ihren neu erstellten Bot als **Administrator** mit der Berechtigung "Nachrichten posten" in alle Kanäle hinzu, die Sie bespielen möchten.
4. **Kanal-IDs ermitteln**:
   - Wenn Ihr Kanal öffentlich ist, ist die ID einfach `@IhrKanalBenutzername` (z. B. `@mein_ki_news_kanal`).
   - Wenn Ihr Kanal privat ist, senden Sie eine Testnachricht im Kanal, leiten Sie sie an einen Bot wie `@JsonDumpBot` weiter, um die `chat.id` (beginnt meist mit `-100...`) zu ermitteln.

### Schritt 2: Gemini API Key erstellen
Erstellen Sie einen API-Key in Google AI Studio, um die Zusammenfassungen zu generieren.

### Schritt 3: `.env` Datei konfigurieren
Erstellen Sie eine `.env`-Datei auf Basis von [`.env.example`](file:///telegram_ai_news_bot/.env.example) und tragen Sie Ihre Werte ein.

Wählen Sie dazu Ihren gewünschten Modus über die Variable `BOT_MODE` aus:

*   **Option A: Nur Deutsch**
    ```env
    BOT_MODE=german_only
    TELEGRAM_BOT_TOKEN=Ihr_Telegram_Bot_Token
    TELEGRAM_CHANNEL_ID_DE=@ihr_deutscher_kanal
    GEMINI_API_KEY=Ihr_Gemini_API_Key
    ```

*   **Option B: Nur Englisch**
    ```env
    BOT_MODE=english_only
    TELEGRAM_BOT_TOKEN=Ihr_Telegram_Bot_Token
    TELEGRAM_CHANNEL_ID_EN=@ihr_englischer_kanal
    GEMINI_API_KEY=Ihr_Gemini_API_Key
    ```

*   **Option C: Zweisprachig in EINEM Kanal (Bilingual Single Channel)**
    *Es wird erst ein deutscher Digest gepostet, gefolgt von einem englischen Digest im selben Kanal.*
    ```env
    BOT_MODE=bilingual_single_channel
    TELEGRAM_BOT_TOKEN=Ihr_Telegram_Bot_Token
    TELEGRAM_CHANNEL_ID=@ihr_gemeinsamer_kanal
    GEMINI_API_KEY=Ihr_Gemini_API_Key
    ```

*   **Option D: Zwei separate Kanäle (Sehr professionell!)**
    *Der deutsche Digest geht in den deutschen Kanal, der englische Digest in den englischen Kanal. Das Skript läuft einmal täglich und erledigt beides auf einmal!*
    ```env
    BOT_MODE=two_channels
    TELEGRAM_BOT_TOKEN=Ihr_Telegram_Bot_Token
    TELEGRAM_CHANNEL_ID_DE=@ihr_deutscher_kanal
    TELEGRAM_CHANNEL_ID_EN=@ihr_englischer_kanal
    GEMINI_API_KEY=Ihr_Gemini_API_Key
    ```

### Schritt 4: Ausführen
Installieren Sie die Abhängigkeiten auf Ihrem PC oder Server:
```bash
pip install -r requirements.txt
```
Führen Sie das Hauptskript aus:
```bash
python main.py
```

---\n\n## ⏰ Wie man es automatisiert (Kostenlos)

Damit das Skript jeden Tag vollautomatisch läuft:

### Über GitHub Actions (Vollständig kostenlos, kein Server benötigt)

GitHub führt das Skript jeden Tag kostenlos auf seinen Servern aus (als Cronjob).

1. Erstellen Sie ein neues privates oder öffentliches Repository auf GitHub.
2. Laden Sie dieses Projekt hoch.
3. Erstellen Sie eine Datei unter `.github/workflows/daily.yml` mit folgendem Inhalt:
   ```yaml
   name: Daily AI News
   on:
     schedule:
       - cron: '0 8 * * *' # Läuft jeden Tag um 08:00 UTC (10:00 Uhr deutsche Zeit)
     workflow_dispatch: # Erlaubt manuelles Ausführen über das Web-UI

   jobs:
     run-bot:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout Code
           uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'

         - name: Install Dependencies
           run: |
             pip install -r requirements.txt

         - name: Run Bot Script
           env:
             TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
             BOT_MODE: ${{ secrets.BOT_MODE }}
             TELEGRAM_CHANNEL_ID: ${{ secrets.TELEGRAM_CHANNEL_ID }}
             TELEGRAM_CHANNEL_ID_DE: ${{ secrets.TELEGRAM_CHANNEL_ID_DE }}
             TELEGRAM_CHANNEL_ID_EN: ${{ secrets.TELEGRAM_CHANNEL_ID_EN }}
             GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
           run: python main.py
   ```
4. Gehen Sie in Ihrem GitHub-Repository auf **Settings -> Secrets and Variables -> Actions** und fügen Sie Ihre Umgebungsvariablen (z. B. `TELEGRAM_BOT_TOKEN`, `BOT_MODE`, `TELEGRAM_CHANNEL_ID_DE`, `TELEGRAM_CHANNEL_ID_EN`, `GEMINI_API_KEY`) als **Repository Secrets** hinzu. Fertig!

---\n\n## 🔗 Die ursprünglichen GitHub-Repositories
Falls Sie sich die Repositories anschauen wollen, auf denen diese Ideen basieren:
1. **[giftedunicorn/ai-news-bot](https://github.com/giftedunicorn/ai-news-bot)** (Verwendet RSS, übersetzt in 13+ Sprachen, läuft via GitHub Actions).
2. **[hrnrxb/AI-News-Aggregator-Bot](https://github.com/hrnrxb/AI-News-Aggregator-Bot)** (Telegram-spezifisch, zieht auch GitHub Trends).
3. **[rrs1979/TelegramChannelAI](https://github.com/rrs1979/TelegramChannelAI)** (Scannt andere Telegram-Kanäle, schreibt sie mit KI um und generiert Flux-Bilder).
