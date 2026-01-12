import hashlib
import json
from datetime import datetime

from app.core.config import CACHE_DIR


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
        "Explique pourquoi les livres proposes correspondent aux preferences. "
        "Donne une synthese courte (6-10 phrases), claire, en francais. "
        "Ne mentionne pas de points techniques.\n\n"
        f"Preferences utilisateur (JSON): {json.dumps(prefs, ensure_ascii=True)}\n"
        "Top livres:\n"
        + "\n".join(books_lines)
    )


def generate_synthesis(prompt, api_key, model_name="gemini-2.5-flash"):
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
