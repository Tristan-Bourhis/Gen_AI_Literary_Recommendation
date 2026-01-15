import numpy as np

from app.core.config import CACHE_DIR
from app.services.referential_loader import load_books
from app.nlp.embeddings import load_embedding_model
from app.nlp.preprocess import normalize


def main():
    books = load_books()
    book_texts = [normalize(f"{book['title']}. {book['summary']}") for book in books]
    model = load_embedding_model()
    embeddings = model.encode(book_texts, fit_texts=book_texts)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CACHE_DIR / "embeddings_books.npy"
    np.save(output_path, embeddings)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
