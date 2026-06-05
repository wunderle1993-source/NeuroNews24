"""
llm_provider.py - Einheitlicher LLM-Zugangspunkt fuer NeuroNews24
Reihenfolge: Groq (primaer) -> Groq Fallback
"""
import json
import os


class ProviderError(RuntimeError):
    pass


def _extract_json(text: str) -> str:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


def _flatten_parts(parts) -> str:
    if isinstance(parts, str):
        return parts
    if not isinstance(parts, list):
        return str(parts)

    result = []
    for item in parts:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            result.append(item.get("text", "[non-text attachment]"))
        else:
            result.append(str(item))
    return "\n".join(result)


def _groq_generate_json(parts, *, api_key: str, temperature: float) -> dict:
    try:
        from groq import Groq
    except ImportError as exc:
        raise ProviderError("groq package is not installed.") from exc

    client = Groq(api_key=api_key)
    prompt = _flatten_parts(parts)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        max_tokens=2048,
        response_format={"type": "json_object"},
    )

    text = response.choices[0].message.content
    if not text:
        raise ProviderError("Groq response did not contain text.")
    return json.loads(_extract_json(text))


def generate_json(parts, *, model: str = "", api_key: str = "", temperature: float = 0.9) -> dict:
    groq_primary = os.getenv("GROQ_API_KEY") or ""
    groq_fallback = os.getenv("GROQ_FALLBACK_KEY") or ""
    _ = api_key

    if groq_primary:
        try:
            print("[LLM] Trying Groq (primary)...")
            result = _groq_generate_json(parts, api_key=groq_primary, temperature=temperature)
            print("[LLM] Groq primary succeeded.")
            return result
        except Exception as exc:
            print(f"[LLM] Groq primary failed: {exc}")
    else:
        print("[LLM] No GROQ_API_KEY configured.")

    if groq_fallback:
        try:
            print("[LLM] Trying Groq (fallback key)...")
            result = _groq_generate_json(parts, api_key=groq_fallback, temperature=temperature)
            print("[LLM] Groq fallback succeeded.")
            return result
        except Exception as exc:
            print(f"[LLM] Groq fallback failed: {exc}")

    raise ProviderError("All configured Groq providers failed.")
