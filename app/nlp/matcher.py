from app.nlp.embeddings import load_embedding_model
from app.nlp.preprocess import normalize
from app.nlp.similarity import cosine_matrix


def match_segments_to_books(segments, books):
    cleaned_segments = [normalize(text) for _, text in segments if text.strip()]
    if not cleaned_segments:
        return {}, None, "none", []

    book_texts = []
    book_ids = []
    for book in books:
        combined = " ".join(
            [
                book.get("title", ""),
                book.get("author", ""),
                book.get("genres", ""),
                book.get("period", ""),
                str(book.get("publication_year_raw", "")),
                " ".join(book.get("keywords", [])),
                book.get("summary", ""),
            ]
        )
        book_texts.append(normalize(combined))
        book_ids.append(book["book_id"])

    model = load_embedding_model()

    if model.mode == "tfidf":
        all_texts = cleaned_segments + book_texts
        embeddings = model.encode(all_texts, fit_texts=all_texts)
        user_emb = embeddings[: len(cleaned_segments)]
        book_emb = embeddings[len(cleaned_segments) :]
    else:
        user_emb = model.encode(cleaned_segments)
        book_emb = model.encode(book_texts)

    similarities = cosine_matrix(user_emb, book_emb)
    scores = similarities.mean(axis=0) if similarities.size else []
    book_scores = {book_id: float(score) for book_id, score in zip(book_ids, scores)}
    return book_scores, similarities, model.mode, book_ids
