import google.generativeai as genai
from config import GEMINI_API_KEY

def summarize_articles(articles, language="German"):
    """
    Uses Gemini API to curate and summarize the list of articles in the specified language.
    Returns a formatted markdown text ready for Telegram posting.
    """
    if not articles:
        return None

    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY is not set. Using a fallback mock summarization.")
        return generate_mock_summary(articles, language)

    genai.configure(api_key=GEMINI_API_KEY)

    # Format the articles for the prompt
    articles_text = ""
    for idx, art in enumerate(articles):
        articles_text += f"Article #{idx+1}\n"
        articles_text += f"Title: {art['title']}\n"
        articles_text += f"Source: {art['source']}\n"
        articles_text += f"Description: {art['summary']}\n"
        articles_text += f"Link: {art['link']}\n"
        articles_text += "-"*40 + "\n"

    # Define language-specific details
    if language.lower() == "german" or language.lower() == "deutsch":
        lang_name = "German (Deutsch)"
        title_example = "🤖 KI DAILY DIGEST - [Datum]"
        link_text = "Quelle"
        takeaway_instruction = "Beende mit einer kurzen täglichen Erkenntnis oder einer Frage, um die Interaktion im Kanal zu fördern."
    else:
        lang_name = "English"
        title_example = "🤖 AI DAILY DIGEST - [Date]"
        link_text = "Source"
        takeaway_instruction = "End with a brief daily takeaway or a question to spark engagement."

    # Construct the system instruction and prompt
    prompt = f"""
You are an edgy, highly connected investigative tech journalist and AI insider. You curate the daily "Underground AI & Tech News" newsletter.
Your task is to analyze the following list of articles fetched from the last 24 hours. You MUST focus heavily on:
1. AI Jailbreaks, exploits, or model bypasses.
2. Leaked models, internal company dramas, or unreleased tech.
3. Crazy, mind-blowing open-source releases (like new LocalLLaMA models).
4. Major cybersecurity incidents related to AI.

Select the top 5 most exciting and controversial stories from the list (ignore boring corporate PR or trivial updates) and write a highly-readable, engaging, and slightly edgy daily digest.

Language requirements:
You MUST write the response entirely in {lang_name}.

Formatting instructions for Telegram Markdown:
- Give the digest a catchy, edgy title (e.g., "{title_example} 💥").
- Use a clean structure. Each of the top 5 news items must have:
  - A dramatic emoji corresponding to the topic (🔥, 🔓, 🚨, 🧠, etc.).
  - A bold title using standard markdown: *Title*
  - A concise, punchy 2-3 sentence summary explaining the leak/news and why it's a big deal.
  - A markdown link to the source: [{link_text}](URL).
- {takeaway_instruction}
- Use simple Telegram-friendly Markdown formatting. Use standard *bold* (single asterisk) and [Link](URL). No backslashes or complex escaping.

Here is the raw news data:
{articles_text}
"""

    try:
        # Changed model from "gemini-1.5-flash" to "gemini-2.5-pro" for better reasoning
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for language {language}: {e}")
        return generate_mock_summary(articles, language)

def generate_mock_summary(articles, language="German"):
    """
    Fallback method to generate a summary if Gemini API is not configured or fails.
    """
    is_de = language.lower() in ["german", "deutsch"]
    
    if is_de:
        output = "🤖 *KI DAILY DIGEST (Fallback)*\n\n"
        output += f"Es wurden {len(articles)} neue Artikel in den letzten 24 Stunden gefunden. Hier sind die Top-Meldungen:\n\n"
        for art in articles[:5]:
            output += f"🔹 *{art['title']}*\n"
            output += f"Quelle: {art['source']}\n"
            output += f"🔗 [Originalen Artikel lesen]({art['link']})\n\n"
        output += "Bitte konfigurieren Sie Ihren `GEMINI_API_KEY` in der `.env`-Datei, um eine vollautomatische, KI-generierte Zusammenfassung auf Deutsch zu erhalten!"
    else:
        output = "🤖 *AI DAILY DIGEST (Fallback)*\n\n"
        output += f"Found {len(articles)} new articles in the last 24 hours. Here are the top stories:\n\n"
        for art in articles[:5]:
            output += f"🔹 *{art['title']}*\n"
            output += f"Source: {art['source']}\n"
            output += f"🔗 [Read original article]({art['link']})\n\n"
        output += "Please configure your `GEMINI_API_KEY` in the `.env` file to get a fully automated, AI-generated summary in English!"
        
    return output
