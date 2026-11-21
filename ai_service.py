"""Gemini wrapper for the doubt solver. All AI calls go through this file."""
import os

import streamlit as st
from google import genai
from google.genai import errors as genai_errors

MODEL_NAME = "gemini-2.5-flash"
MAX_DOC_CHARS = 30000
MAX_HISTORY_MESSAGES = 6

SYSTEM_RULES = """You are EduSpark AI, a patient tutor for college students.
Rules:
- If DOCUMENT TEXT is given, answer from it first and say which part of it you used.
- If the document does not contain the answer, say so clearly, then give a general explanation under the heading "General explanation (not from your document)".
- Never invent facts about the document.
- For numerical or problem-solving questions, show step-by-step working.
- Explain hard topics in simple English first, with one short example.
"""


class AIServiceError(Exception):
    """An error the user can read. Shown in the app as-is."""


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
        except Exception:
            key = ""
    if not key:
        raise AIServiceError(
            "AI is not set up yet: GEMINI_API_KEY is missing. "
            "On Replit, add it under Tools > Secrets. "
            "On Streamlit Cloud, add it under app Settings > Secrets."
        )
    return key


def build_prompt(question, language, document_text, history):
    parts = [SYSTEM_RULES]
    if language == "English":
        parts.append("Answer language: English.")
    else:
        parts.append(f"Answer language: {language}. Keep technical terms in English, in brackets.")
    if document_text:
        parts.append("DOCUMENT TEXT (may be cut short):\n<<<\n" + document_text[:MAX_DOC_CHARS] + "\n>>>")
    if history:
        recent = history[-MAX_HISTORY_MESSAGES:]
        parts.append("Recent conversation:\n" + "\n".join(f"{role}: {text}" for role, text in recent))
    parts.append("STUDENT QUESTION:\n" + question)
    return "\n\n".join(parts)


def ask_gemini(question, language="English", document_text=None, history=None):
    client = genai.Client(api_key=get_api_key())
    prompt = build_prompt(question, language, document_text, history or [])
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    except genai_errors.APIError as exc:
        code = getattr(exc, "code", None)
        if code == 429:
            raise AIServiceError("Gemini rate limit reached (free tier). Wait a minute, then try again.") from exc
        if code in (404, 503):
            raise AIServiceError("The Gemini model is unavailable right now. Try again in a few minutes.") from exc
        raise AIServiceError(f"Gemini returned an error ({code}). Check your API key and try again.") from exc
    except Exception as exc:
        raise AIServiceError("Could not reach Gemini. Check your internet connection and try again.") from exc
    answer = (response.text or "").strip()
    if not answer:
        raise AIServiceError("Gemini returned an empty answer. Try rephrasing the question.")
    return answer
