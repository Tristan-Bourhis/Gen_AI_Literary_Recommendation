from app.domain.schemas import BookReco

MATCH_PERCENT_FLOOR = 15
MATCH_PERCENT_CEILING = 99


def _score_to_match_percent(score, score_min, score_max):
    """Convertit un score brut (similarite + bonus) en pourcentage lisible.

    Le score brut combine une similarite cosinus (rarement > 0.5) et des
    bonus/malus additifs : affiche tel quel, le meilleur resultat semble
    "mauvais" (ex. 31%). On re-echelonne donc le score par rapport a la
    distribution des candidats du referentiel, pour qu'un "bon match" se lise
    comme un vrai pourcentage de correspondance (proche de 90-99%) plutot que
    comme la valeur brute du calcul interne.
    """
    if score_max <= score_min:
        return MATCH_PERCENT_CEILING
    ratio = (score - score_min) / (score_max - score_min)
    ratio = min(1.0, max(0.0, ratio))
    percent = MATCH_PERCENT_FLOOR + ratio * (MATCH_PERCENT_CEILING - MATCH_PERCENT_FLOOR)
    return round(percent)


def recommend_books(book_scores, books, top_n=10, breakdowns=None, segment_matches=None):
    ranked = sorted(book_scores.items(), key=lambda item: item[1], reverse=True)
    all_scores = list(book_scores.values())
    score_min = min(all_scores) if all_scores else 0.0
    score_max = max(all_scores) if all_scores else 1.0

    results = []
    for book_id, score in ranked[:top_n]:
        book = next((item for item in books if item["book_id"] == book_id), None)
        if not book:
            continue
        breakdown = breakdowns.get(book_id) if breakdowns else None
        matches = segment_matches.get(book_id) if segment_matches else None
        results.append(
            BookReco(
                book_id=book_id,
                title=book["title"],
                score=score,
                author=book.get("author", ""),
                publication_year=book.get("publication_year"),
                publication_year_raw=book.get("publication_year_raw", ""),
                genres=book.get("genres", ""),
                period=book.get("period", ""),
                summary=book.get("summary", ""),
                score_breakdown=breakdown,
                segment_matches=matches,
                match_percent=_score_to_match_percent(score, score_min, score_max),
            )
        )
    return results
