"""
FREE multilingual translation agent.
No Gemini API required.
"""

from __future__ import annotations

from deep_translator import GoogleTranslator
from langdetect import detect


# ─────────────────────────────────────────────────────────────

def translate_text(
    user_input: str,
    target_lang: str,
) -> dict:

    try:
        detected = detect(user_input)

    except Exception:
        detected = "unknown"

    try:
        translated = GoogleTranslator(
            source="auto",
            target=target_lang.lower()
        ).translate(user_input)

    except Exception as e:

        return {
            "detected_language": detected,
            "target_language": target_lang,
            "translation": f"Translation Error: {e}",
            "rag_note": "Translation failed.",
            "chunks_added": 0,
            "explanation": None,
        }

    return {
        "detected_language": detected,
        "target_language": target_lang,
        "translation": translated,
        "rag_note": "Free translation completed successfully.",
        "chunks_added": 1,
        "explanation": None,
    }