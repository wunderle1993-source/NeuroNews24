from llm_provider import generate_json
import os


def _build_enforced_footer(articles, language="German") -> str:
    joined = " ".join(
        f"{art.get('title', '')} {art.get('summary', '')}" for art in (articles or [])[:8]
    ).lower()

    if any(token in joined for token in ["attack", "cyber", "exploit", "cisa", "warn", "breach"]):
        risk_line_de = (
            "Heute sieht man, wie schnell aus Technikmeldungen echte Sicherheitslagen werden: "
            "offene Systeme, billige Automatisierung und schlechte Absicherung schaffen reale Angriffsfenster."
        )
        risk_line_en = (
            "Today's pattern shows how fast technical news turns into real security exposure: "
            "open systems, cheap automation, and weak defenses create live attack windows."
        )
    elif any(token in joined for token in ["jailbreak", "leak", "uncensored", "open model", "weights"]):
        risk_line_de = (
            "Die eigentliche Sprengkraft liegt darin, dass offene oder geleakte Modelle Macht verteilen: "
            "mehr Freiheit fuer Forscher, aber auch mehr Reichweite fuer Missbrauch und Manipulation."
        )
        risk_line_en = (
            "The real shockwave is that open or leaked models redistribute power: "
            "more freedom for researchers, but also more reach for misuse and manipulation."
        )
    else:
        risk_line_de = (
            "Die groesste Gefahr ist nicht eine einzelne Nachricht, sondern die Beschleunigung: "
            "Faehigkeiten, die gestern noch Spezialwissen waren, koennen morgen Massenwerkzeuge sein."
        )
        risk_line_en = (
            "The biggest danger is not one single headline but the speed of change: "
            "capabilities that required specialists yesterday can become mass-market tools tomorrow."
        )

    if language.lower() in {"german", "deutsch"}:
        return (
            "\n\n<b>NeuroNews24 Fazit</b>\n"
            f"<blockquote>{risk_line_de} "
            "Wer sich schuetzen will, sollte auf Warnzeichen, neue Missbrauchsmuster und ploetzliche Faehigkeitsspruenge achten, "
            "statt erst zu reagieren, wenn der Schaden schon sichtbar ist.</blockquote>"
        )

    return (
        "\n\n<b>NeuroNews24 Take</b>\n"
        f"<blockquote>{risk_line_en} "
        "Anyone trying to stay protected should watch for warning signs, new misuse patterns, and sudden capability jumps "
        "instead of waiting until the damage is already visible.</blockquote>"
    )


def _ensure_editorial_footer(text: str, articles, language="German") -> str:
    if not text:
        return _build_enforced_footer(articles, language)

    marker = "NeuroNews24 Fazit" if language.lower() in {"german", "deutsch"} else "NeuroNews24 Take"
    if marker.lower() in text.lower():
        return text

    return text.rstrip() + _build_enforced_footer(articles, language)


def summarize_articles(articles, language="German"):
    """
    Uses the shared LLM provider to generate summaries.
    Returns Telegram-ready HTML.
    """
    if not articles:
        return None

    llm_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_FALLBACK_KEY")
    if not llm_key:
        print("Warning: No LLM API key is set in .env.")
        return generate_mock_summary(articles, language)

    articles_text = ""
    for idx, art in enumerate(articles):
        articles_text += f"Article #{idx+1}\n"
        articles_text += f"Title: {art['title']}\n"
        articles_text += f"Source: {art['source']}\n"
        articles_text += f"Description: {art['summary']}\n"
        articles_text += f"Link: {art['link']}\n"
        articles_text += "-" * 40 + "\n"

    if language.lower() in {"german", "deutsch"}:
        lang_name = "German (Deutsch)"
        title_example = "NeuroNews24 | KI Daily Brief"
        link_text = "Quelle"
        takeaway_instruction = (
            "Beende mit genau einem starken Footer-Block namens "
            "<b>NeuroNews24 Fazit</b>. In diesem Fazit sollst du kurz und pointiert erklaeren: "
            "Warum ist das heute relevant, welches Risiko oder welche Macht steckt darin, "
            "was koennte daraus in der echten Welt entstehen, und warum sollten Leser aufhorchen. "
            "Der Ton darf schaerfer, dramatischer und spannender sein, aber er muss sachlich bleiben. "
            "Erklaere Gefahren so, dass auch Nicht-Experten sie sofort verstehen. "
            "Erlaube konkrete Aufklaerung, defensive Warnzeichen, Missbrauchsmuster und Schutz-Hinweise, "
            "aber keine operative Schritt-fuer-Schritt-Anleitung fuer Angriffe oder Missbrauch."
        )
    else:
        lang_name = "English"
        title_example = "NeuroNews24 | AI Daily Brief"
        link_text = "Source"
        takeaway_instruction = (
            "End with exactly one strong footer block named "
            "<b>NeuroNews24 Take</b>. This section should explain why today's stories matter, "
            "what power or risk they unlock, what could realistically emerge from them in the real world, "
            "and why readers should pay attention. The tone may be sharper and more dramatic, but it must stay factual. "
            "Explain risks so non-experts can understand them immediately. "
            "Allow concrete defensive warning signs, misuse patterns, and protection cues, "
            "but no operational step-by-step attack guidance."
        )

    system_prompt = f"""
You are an investigative AI and tech editor with sharp taste and zero patience for boring PR.
Analyze the following article list from the last 24 hours.
Prioritize:
1. model leaks, jailbreaks, exploits, internal drama
2. wild open-source releases
3. surprising AI security incidents
4. only the most relevant AI stories readers will actually talk about

Language requirements:
You MUST write the response entirely in {lang_name}.

Formatting instructions for Telegram HTML:
- Start with a strong branded headline like <b>{title_example}</b>
- Add a short italic subheader line
- Choose the top 5 most interesting stories
- For each story use:
  - a fitting emoji
  - <b>Title</b>
  - a 2-3 sentence crisp summary
  - an inline HTML source link: <a href="URL">{link_text}</a>
- Where appropriate, briefly explain what this could enable, why it is dangerous, or what defenders should watch for
- End with a short takeaway section
- Put the takeaway only once, as a footer, not in both header and footer
- Use only Telegram-safe HTML: <b>, <i>, <a>, <blockquote>
- Do NOT use Markdown
- Keep the full output below 3600 characters

CRITICAL:
Return valid JSON with exactly one key named "summary".
"""

    prompt = f"Here is the raw news data:\n{articles_text}"

    try:
        print("Using llm_provider (Groq primary -> Groq fallback)...")
        response_dict = generate_json(
            parts=[system_prompt, prompt],
            model="llama-3.3-70b-versatile",
            api_key=llm_key,
            temperature=0.7,
        )
        response_text = response_dict.get("summary", "")
        response_text = _ensure_editorial_footer(response_text, articles, language)
        print("  API successful.")
        return response_text
    except Exception as e:
        print(f"API failed: {e}")
        return generate_mock_summary(articles, language)


def generate_mock_summary(articles, language="German"):
    is_de = language.lower() in ["german", "deutsch"]

    if is_de:
        output = "<b>NeuroNews24 | Fallback Briefing</b>\n\n"
        output += f"<i>{len(articles)} relevante Artikel in den letzten 24 Stunden gefunden.</i>\n\n"
        for art in articles[:5]:
            output += f"• <b>{art['title']}</b>\n"
            output += f"{art['source']} | <a href=\"{art['link']}\">Quelle</a>\n\n"
        output += (
            "<b>NeuroNews24 Fazit</b>\n"
            "<blockquote>Heute faellt auf, wie schnell aus scheinbar technischer AI-News echte Machtfragen werden: "
            "Modelle, Leaks und offene Tools koennen in kuerzester Zeit von Experimenten zu Risiko-Multiplikatoren werden. "
            "Wer diese Entwicklung unterschaetzt, wacht spaeter in einer Welt auf, in der Missbrauch, Ueberwachung oder Manipulation "
            "viel billiger und schneller geworden sind.</blockquote>\n\n"
        )
        output += "<blockquote>Fallback-Modus aktiv. Der Kanal bleibt auf stabilen Primary- und Secondary-Provider ausgerichtet und soll ohne sichtbare Notfalltexte sauber weiterlaufen.</blockquote>"
    else:
        output = "<b>NeuroNews24 | Fallback Briefing</b>\n\n"
        output += f"<i>Found {len(articles)} relevant articles in the last 24 hours.</i>\n\n"
        for art in articles[:5]:
            output += f"• <b>{art['title']}</b>\n"
            output += f"{art['source']} | <a href=\"{art['link']}\">Source</a>\n\n"
        output += (
            "<b>NeuroNews24 Take</b>\n"
            "<blockquote>Today's pattern is simple: what looks like niche AI news can quickly become real leverage. "
            "Leaks, open models, and jailbreak-adjacent tools can shift power fast, lower the barrier for abuse, "
            "and make manipulation or surveillance cheaper than most people expect.</blockquote>\n\n"
        )
        output += "<blockquote>Fallback mode active. The channel stays aligned to a stable primary and secondary provider path and should continue without noisy recovery text.</blockquote>"

    return output
