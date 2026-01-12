import unittest

from app.domain.scoring import compute_coverage


class ScoringTests(unittest.TestCase):
    def test_compute_coverage(self):
        scores = [0.8, 0.6, 0.4, 0.2]
        self.assertAlmostEqual(compute_coverage(scores, top_k=2), 70.0)


if __name__ == "__main__":
    unittest.main()
