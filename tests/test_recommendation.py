import unittest

from app.domain.recommendation import recommend_books


class RecommendationTests(unittest.TestCase):
    def test_recommend_books(self):
        book_scores = {"B001": 0.9, "B002": 0.1}
        books = [
            {
                "book_id": "B001",
                "title": "Livre 01",
                "author": "Auteur A",
                "publication_year": 2001,
                "publication_year_raw": "2001",
                "genres": "fantasy",
                "period": "classique",
                "keywords": ["aventure"],
                "summary": "Aventure heroique.",
            },
            {
                "book_id": "B002",
                "title": "Livre 02",
                "author": "Auteur B",
                "publication_year": 2005,
                "publication_year_raw": "2005",
                "genres": "realiste",
                "period": "contemporain",
                "keywords": ["quotidien"],
                "summary": "Recit sobre.",
            },
        ]
        results = recommend_books(book_scores, books, top_n=1)
        self.assertEqual(results[0].book_id, "B001")


if __name__ == "__main__":
    unittest.main()
