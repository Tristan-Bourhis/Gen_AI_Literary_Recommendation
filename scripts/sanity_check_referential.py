from app.services.referential_loader import load_books, load_questions


def check_books(books):
    required = {
        "book_id",
        "title",
        "author",
        "publication_year",
        "genres",
        "period",
        "keywords",
        "summary",
    }
    for idx, book in enumerate(books, start=1):
        missing = required - set(book.keys())
        if missing:
            raise ValueError(f"Book {idx} missing keys: {missing}")
    if len(books) < 60:
        raise ValueError("Le referentiel doit contenir au moins 60 livres.")


def check_questions(questions):
    required = {"id", "section", "type", "label"}
    for idx, question in enumerate(questions, start=1):
        missing = required - set(question.keys())
        if missing:
            raise ValueError(f"Question {idx} missing keys: {missing}")


def main():
    check_books(load_books())
    check_questions(load_questions())
    print("Referential OK")


if __name__ == "__main__":
    main()
