import hashlib
import json
import os
from datetime import datetime

from dotenv import load_dotenv

from app.core.config import CACHE_DIR, ROOT_DIR

load_dotenv(dotenv_path=ROOT_DIR / ".env")


def _load_cache(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_cache(path, payload):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2)


def _prompt_hash(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def build_synthesis_prompt(answers, book_recos):
    top_books = book_recos[:5]
    books_lines = []
    for idx, book in enumerate(top_books, start=1):
        books_lines.append(
            f"{idx}. {book.title} | {book.author} | {book.period}"
        )

    prefs = {
        "texte_libre": answers.get("free_1", ""),
        "auteurs_aimes": answers.get("free_2", ""),
        "eviter": answers.get("free_3", ""),
        "auteur_favori": answers.get("auteur_favori", ""),
        "complexite": answers.get("complexite", ""),
        "rythme": answers.get("rythme", ""),
        "poetique": answers.get("poetique", ""),
        "realiste": answers.get("realiste", ""),
        "personnages": answers.get("personnages", ""),
        "intrigue": answers.get("intrigue", ""),
        "genre": answers.get("genre", []),
        "periode": answers.get("periode", ""),
        "themes": answers.get("themes", []),
        "format": answers.get("format", ""),
    }

    return (
        "Tu es un assistant de recommandation litteraire. "
        "Fournis une analyse des resultats affiches a l'utilisateur. "
        "1) Explique pourquoi chaque livre recommande correspond aux preferences. "
        "2) Donne une lecture rapide des graphiques: radar des preferences, carte semantique "
        "(ambiance vs densite), top genres, heatmap des criteres. "
        "3) Termine par une synthese claire. "
        "Ecris en francais, ton naturel, 10-14 phrases max. "
        "Ne mentionne pas de points techniques ni de JSON.\n\n"
        f"Preferences utilisateur (JSON): {json.dumps(prefs, ensure_ascii=True)}\n"
        "Top livres:\n"
        + "\n".join(books_lines)
    )


def _get_gemini_key():
    return (
        os.getenv("GEMINI")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )


def _get_gemini_model_name():
    env_model = os.getenv("GEMINI_MODEL_NAME") or os.getenv("GEMINI_MODEL")
    if env_model:
        return env_model
    fallback = os.getenv("MODEL_NAME")
    if fallback and fallback.lower().startswith("gemini-"):
        return fallback
    return None


def generate_synthesis(prompt, api_key=None, model_name=None):
    if not model_name:
        model_name = _get_gemini_model_name() or "gemini-2.5-flash"
    if not api_key:
        api_key = _get_gemini_key()
    if not api_key:
        raise ValueError("Missing GEMINI API key in environment.")

    cache_path = CACHE_DIR / "genai_cache.json"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = _load_cache(cache_path)
    key = _prompt_hash(prompt)
    if key in cache:
        return cache[key]["response"], True

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    text = response.text.strip()
    cache[key] = {
        "response": text,
        "created_at": datetime.utcnow().isoformat(),
        "model": model_name,
    }
    _save_cache(cache_path, cache)
    return text, False


def translate_to_french(text, api_key=None, model_name=None):
    if not text:
        return text
    if not model_name:
        model_name = _get_gemini_model_name() or "gemini-2.5-flash"
    if not api_key:
        api_key = _get_gemini_key()
    if not api_key:
        raise ValueError("Missing GEMINI API key in environment.")

    cache_path = CACHE_DIR / "translation_cache.json"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = _load_cache(cache_path)
    key = _prompt_hash(f"{model_name}:{text}")
    if key in cache:
        return cache[key]["response"]

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    prompt = (
        "Translate the following book summary to French. "
        "Keep proper nouns and titles unchanged. "
        "Return only the translation.\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    translated = response.text.strip()
    cache[key] = {
        "response": translated,
        "created_at": datetime.utcnow().isoformat(),
        "model": model_name,
    }
    _save_cache(cache_path, cache)
    return translated
