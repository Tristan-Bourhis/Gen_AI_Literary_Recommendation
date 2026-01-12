import unittest

from app.nlp.matcher import match_segments_to_books


class MatcherTests(unittest.TestCase):
    def test_match_segments_to_books(self):
        segments = [("Livre", "Un monde imaginaire plein d'aventure")]
        books = [
            {
                "book_id": "B001",
                "title": "Livre 01",
                "author": "Auteur A",
                "summary": "Un monde imaginaire et une quete heroique.",
                "period": "classique",
                "keywords": ["aventure"],
                "genres": "fantasy",
            },
            {
                "book_id": "B002",
                "title": "Livre 02",
                "author": "Auteur B",
                "summary": "Recit sobre de la vie quotidienne.",
                "period": "contemporain",
                "keywords": ["quotidien"],
                "genres": "realiste",
            },
        ]
        block_scores, similarities, mode = match_segments_to_books(segments, books)
        self.assertIn("B001", block_scores)
        self.assertIn("B002", block_scores)
        self.assertIsNotNone(similarities)
        self.assertIn(mode, {"sbert", "tfidf", "none"})


if __name__ == "__main__":
    unittest.main()
