import csv
import re

from app.core.config import REFERENTIAL_DIR
from app.core.utils import read_json


def _parse_year(date_str):
    if not date_str:
        return None
    match = re.search(r"(\\d{4})", date_str)
    return int(match.group(1)) if match else None


def _period_from_year(year):
    if not year:
        return "indifferent"
    if year >= 2000:
        return "contemporain"
    if year >= 1900:
        return "20e"
    if year >= 1800:
        return "19e"
    return "classique"


def _keywords_from_text(text):
    if not text:
        return []
    tokens = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return list(dict.fromkeys(tokens))[:10]


def load_books():
    path = REFERENTIAL_DIR / "books_reference.csv"
    books = []
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cleaned = {
                (key or "").strip(): (value or "").strip() for key, value in row.items()
            }
            raw_year = cleaned.get("publication_year", "")
            year = _parse_year(raw_year)
            title = cleaned.get("title", "")
            author = cleaned.get("author", "")
            genres = cleaned.get("genres", "")
            summary = cleaned.get("summary", "")
            if year is None and summary:
                year = _parse_year(summary)
            keywords = _keywords_from_text(f"{title} {author} {genres} {summary}")
            books.append(
                {
                    "book_id": cleaned.get("book_id", ""),
                    "title": title,
                    "author": author,
                    "publication_year": year,
                    "publication_year_raw": raw_year,
                    "genres": genres,
                    "period": _period_from_year(year),
                    "keywords": keywords,
                    "summary": summary or f"{title} par {author}.",
                }
            )
    return books


def load_questions():
    return read_json(REFERENTIAL_DIR / "questions.json")
