from app.domain.schemas import BookReco


def recommend_books(book_scores, books, top_n=10):
    ranked = sorted(book_scores.items(), key=lambda item: item[1], reverse=True)
    results = []
    for book_id, score in ranked[:top_n]:
        book = next((item for item in books if item["book_id"] == book_id), None)
        if not book:
            continue
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
            )
        )
    return results
