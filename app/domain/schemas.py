from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Question:
    id: str
    section: str
    qtype: str
    label: str
    options: List[str] | None = None
    min_value: int | None = None
    max_value: int | None = None
    default: int | None = None


@dataclass(frozen=True)
class Answer:
    question_id: str
    value: str | int | list


@dataclass(frozen=True)
class Book:
    book_id: str
    title: str
    author: str
    publication_year: int | None
    publication_year_raw: str
    genres: str
    period: str
    keywords: List[str]
    summary: str


@dataclass(frozen=True)
class BookReco:
    book_id: str
    title: str
    score: float
    author: str
    publication_year: int | None
    publication_year_raw: str
    genres: str
    period: str
    summary: str
