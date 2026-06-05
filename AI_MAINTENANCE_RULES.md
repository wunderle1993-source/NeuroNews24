# CRITICAL MAINTENANCE RULES FOR NEURONEWS24

Read this before changing anything.

## 1. Configuration Contract
- `load_dotenv(override=True)` is mandatory in `config.py`.
- Primary LLM path is:
  1. `GROQ_API_KEY`
  2. `GROQ_FALLBACK_KEY`
- Never place an `AIza...` Google key into `GROQ_API_KEY` or `GROQ_FALLBACK_KEY`.
- `main.py` must fail fast on invalid config by calling `validate_runtime_config()`.

## 2. Output Contract
- Telegram text output uses `parse_mode="HTML"`.
- Allowed tags are intentionally narrow: `<b>`, `<i>`, `<a>`, `<blockquote>`.
- Do not switch this bot back to Markdown.
- If the LLM prompt changes, keep the JSON contract intact: the provider must still return `{"summary": "..."}`.
- Keep exactly one branded takeaway block at the end of the post:
  - German: `<b>NeuroNews24 Fazit</b>`
  - English: `<b>NeuroNews24 Take</b>`
- Do not duplicate the takeaway in both header and footer.
- The takeaway should feel sharp and memorable, but must not become a misuse tutorial.

## 3. Media Contract
- Do not send a separate hero image before the digest.
- Rely on Telegram's normal link preview behavior inside the message.
- If someone wants image-first posts again later, that must be an explicit product decision, not an automatic feed behavior.

## 4. Stability First
- Do not remove Groq fallback behavior.
- Do not silently rewire provider order.
- Do not add new providers without updating this file and `config.py` validation rules.
- Do not reintroduce any third provider into the live path without an explicit product decision.

## 5. Documentation Truth Rule
- `.env.example`, `README.md`, and startup helpers must reflect the live provider contract.
- If the runtime uses Groq-first, the docs must also say Groq-first.

## 6. Scheduling Rule
- Standardbetrieb ist 2x taeglich: 08:30 und 17:00.
- Vor jedem Live-Post muss der `post_guard.py` Schutz greifen.
- Vor jedem Live-Run muss der `run_lock.py` Schutz greifen, damit keine ueberlappenden Doppelstarts passieren.
