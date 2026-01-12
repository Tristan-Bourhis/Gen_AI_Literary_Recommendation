from app.domain.profiling import compute_coverage
from app.domain.recommendation import recommend_books
from app.nlp.matcher import match_segments_to_books


def scale_descriptor(label, value):
    levels = {
        1: "tres faible",
        2: "faible",
        3: "modere",
        4: "eleve",
        5: "tres eleve",
    }
    return f"{label} {levels.get(value, value)}"


def build_segments(answers):
    segments = []
    segments.append(("Livre ideal", answers.get("free_1", "")))
    segments.append(("Auteurs preferes", answers.get("free_2", "")))
    segments.append(("A eviter", answers.get("free_3", "")))
    if answers.get("auteur_favori"):
        segments.append(("Auteur favori", answers.get("auteur_favori", "")))
    segments.append(("Complexite", scale_descriptor("complexite", answers.get("complexite", 3))))
    segments.append(("Rythme", scale_descriptor("rythme", answers.get("rythme", 3))))
    segments.append(
        ("Style poetique", scale_descriptor("style poetique", answers.get("poetique", 3)))
    )
    segments.append(
        ("Style realiste", scale_descriptor("style realiste", answers.get("realiste", 3)))
    )
    segments.append(
        (
            "Importance personnages",
            scale_descriptor("personnages", answers.get("personnages", 3)),
        )
    )
    segments.append(
        ("Importance intrigue", scale_descriptor("intrigue", answers.get("intrigue", 3)))
    )
    if answers.get("genre"):
        segments.append(("Genres", " ".join(answers["genre"])))
    if answers.get("periode"):
        segments.append(("Periode", answers["periode"]))
    if answers.get("themes"):
        segments.append(("Themes", " ".join(answers["themes"])))
    if answers.get("format"):
        segments.append(("Format", answers["format"]))
    return segments


def _normalize_tokens(value):
    if not value:
        return []
    if isinstance(value, list):
        return [item.strip().lower() for item in value if str(item).strip()]
    return [item.strip().lower() for item in str(value).replace("|", ";").split(";") if item.strip()]


def _apply_preference_boosts(book_scores, books, answers):
    genres_pref = set(_normalize_tokens(answers.get("genre", [])))
    period_pref = str(answers.get("periode", "")).strip().lower()
    author_pref = str(answers.get("auteur_favori", "")).strip().lower()
    themes_pref = set(_normalize_tokens(answers.get("themes", [])))
    avoid_terms = set(_normalize_tokens(answers.get("free_3", "")))

    boosted = {}
    for book in books:
        book_id = book.get("book_id", "")
        base = book_scores.get(book_id, 0.0)
        pref_score = 0.0

        book_genres = set(_normalize_tokens(book.get("genres", "")))
        book_text = " ".join(
            [
                book.get("title", ""),
                book.get("author", ""),
                book.get("genres", ""),
                book.get("summary", ""),
            ]
        ).lower()

        if genres_pref and book_genres and genres_pref.intersection(book_genres):
            pref_score += 0.4

        if period_pref and period_pref != "indifferent":
            if period_pref == str(book.get("period", "")).strip().lower():
                pref_score += 0.2

        if author_pref and author_pref in str(book.get("author", "")).lower():
            pref_score += 0.4

        if themes_pref:
            theme_hits = [theme for theme in themes_pref if theme in book_text]
            if theme_hits:
                pref_score += min(0.2, 0.05 * len(theme_hits))

        if avoid_terms:
            avoid_hits = [term for term in avoid_terms if term in book_text]
            if avoid_hits:
                pref_score -= min(0.6, 0.2 * len(avoid_hits))

        combined = (0.3 * base) + (0.7 * max(0.0, pref_score))
        boosted[book_id] = min(1.0, max(0.0, combined))
    return boosted


def run_pipeline(answers, books):
    segments = build_segments(answers)
    book_scores, similarities, mode = match_segments_to_books(segments, books)
    if not book_scores:
        return None, None, None, None, mode
    book_scores = _apply_preference_boosts(book_scores, books, answers)
    coverage = compute_coverage(list(book_scores.values()))
    book_recos = recommend_books(book_scores, books)
    return segments, coverage, book_recos, similarities, mode
