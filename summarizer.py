import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from config import GEMINI_API_KEY


def summarize_articles(articles, language="German"):
    """
    Uses Gemini 2.5 Flash to curate and summarize articles.
    Returns formatted Telegram markdown (max ~3800 chars).
    """
    if not articles:
        return None

    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set. Using fallback summary.")
        return generate_mock_summary(articles, language)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build articles text (limit to 30 most recent to save tokens)
    articles_text = ""
    for idx, art in enumerate(articles[:30]):
        articles_text += f"Article #{idx+1}\n"
        articles_text += f"Title: {art['title']}\n"
        articles_text += f"Source: {art['source']}\n"
        articles_text += f"Description: {art['summary']}\n"
        articles_text += f"Link: {art['link']}\n"
        articles_text += "-" * 40 + "\n"

    if language.lower() in ["german", "deutsch"]:
        lang_name      = "German (Deutsch)"
        title_example  = "KI DAILY DIGEST"
        link_text      = "Quelle"
        call_to_action = "Schreib am Ende eine kurze, provokante Frage oder Einschaetzung (1 Satz), die Leser zum Nachdenken bringt."
    else:
        lang_name      = "English"
        title_example  = "AI DAILY DIGEST"
        link_text      = "Source"
        call_to_action = "End with a punchy one-sentence takeaway or question to spark engagement."

    prompt = f"""You are an edgy, investigative tech journalist covering the AI underground.
You write for a Telegram channel called NeuroNews24.

TASK: Analyze the {len(articles[:30])} articles below and pick the TOP 5 most explosive stories.

PRIORITY (most important first):
1. AI Jailbreaks, model exploits, safety bypasses, prompt injection
2. Leaked models, unreleased tech, whistleblower stories, internal drama
3. Mind-blowing open-source drops (LocalLLaMA, Hugging Face, GitHub)
4. Major cybersecurity incidents involving AI systems
5. New model releases breaking benchmarks (GPT, Claude, Gemini, Llama, etc.)

SKIP: boring corporate PR, incremental version bumps, obvious marketing.

LANGUAGE: Write 100% in {lang_name}. No mixing languages.

FORMAT (strict Telegram Markdown):
Line 1: *NEURONEWS24* -- [DD.MM.YYYY HH:MM UTC]
Line 2: One punchy intro sentence (edgy, not corporate)
Blank line
5 stories, each:
  [emoji] *Story Title*
  2-3 sentence summary. What happened? Why does it matter? What's the real impact?
  [{link_text}](<URL>)
  (blank line between stories)
{call_to_action}

HARD LIMIT: Total output must be under 3800 characters.

NEWS DATA:
{articles_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        result = response.text
        print(f"  Gemini (gemini-2.5-flash) generated digest ({len(result)} chars).")
        return result
    except Exception as e:
        print(f"  Gemini API error: {e}")
        return generate_mock_summary(articles, language)


def generate_mock_summary(articles, language="German"):
    is_de = language.lower() in ["german", "deutsch"]
    if is_de:
        out = "*NEURONEWS24* -- Fallback Digest\n\n"
        out += f"Heute: {len(articles)} Artikel analysiert.\n\n"
        for art in articles[:5]:
            out += f"*{art['title']}*\n"
            out += f"Quelle: {art['source']}\n"
            out += f"[Artikel lesen]({art['link']})\n\n"
        out += "_Bitte GEMINI_API_KEY setzen fuer vollstaendige KI-Analyse._"
    else:
        out = "*NEURONEWS24* -- Fallback Digest\n\n"
        out += f"Today: {len(articles)} articles analyzed.\n\n"
        for art in articles[:5]:
            out += f"*{art['title']}*\nSource: {art['source']}\n[Read]({art['link']})\n\n"
        out += "_Please set GEMINI_API_KEY for full AI-powered analysis._"
    return out
