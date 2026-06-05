# NeuroNews24

Mehrsprachiger Telegram-Bot fuer taegliche AI-News. Die Live-Route ist jetzt bewusst auf Stabilitaet ausgelegt:

1. `GROQ_API_KEY`
2. `GROQ_FALLBACK_KEY`

Der Bot kann:
- nur Deutsch posten
- nur Englisch posten
- beide Sprachen in einem Kanal posten
- Deutsch und Englisch auf zwei getrennte Kanaele verteilen

## Wichtige Betriebsregel

NeuroNews24 ist ein HTML-Bot, kein Markdown-Bot.
Die Digest-Ausgabe wird fuer Telegram mit sicheren HTML-Tags formatiert. Das soll nicht wieder auf Markdown zurueckgedreht werden.

## Einrichtung

Beispiel `.env`:

```env
BOT_MODE=two_channels
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID_DE=@your_german_channel
TELEGRAM_CHANNEL_ID_EN=@your_english_channel
GROQ_API_KEY=your_primary_groq_key_here
GROQ_FALLBACK_KEY=your_secondary_groq_key_here
```

## Start

```bash
pip install -r requirements.txt
python main.py
```

## Automation

Fuer lokale Runs kann Windows Task Scheduler genutzt werden.
Fuer Cloud-Automation muessen dieselben Secrets hinterlegt werden:

- `TELEGRAM_BOT_TOKEN`
- `BOT_MODE`
- `TELEGRAM_CHANNEL_ID`
- `TELEGRAM_CHANNEL_ID_DE`
- `TELEGRAM_CHANNEL_ID_EN`
- `GROQ_API_KEY`
- `GROQ_FALLBACK_KEY`

## Pflichtlekture fuer spaetere Agenten

Vor Aenderungen immer lesen:

- [AI_MAINTENANCE_RULES.md](C:/Users/DAGOBERT/Desktop/claudes%20bots/NeuroNews24/AI_MAINTENANCE_RULES.md)
