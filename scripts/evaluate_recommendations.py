"""Evaluation quantitative du moteur de recommandation (hors GenAI).

Teste plusieurs profils utilisateurs types contre le referentiel reel,
mesure la Precision@k sur la correspondance de genre/theme dans le top-k,
et compare au resultat attendu d'une selection aleatoire (baseline).

Usage:
    python scripts/evaluate_recommendations.py
"""
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.nlp.pipeline import run_pipeline
from app.services.referential_loader import load_books

TOP_K = 5

PROFILES = [
    {
        "name": "Thriller a suspense",
        "answers": {
            "free_1": "Je veux un thriller avec beaucoup de rebondissements et de suspense",
            "free_2": "",
            "free_3": "",
            "genre": ["Thriller"],
            "periode": "Peu importe",
            "themes": ["Vengeance", "Secret"],
        },
        "expected_keywords": ["thriller", "suspense", "crime", "mystery", "detective"],
    },
    {
        "name": "Fantasy epique",
        "answers": {
            "free_1": "Je cherche une grande aventure fantastique avec de la magie",
            "free_2": "",
            "free_3": "",
            "genre": ["Fantasy"],
            "periode": "Peu importe",
            "themes": ["Quete", "Pouvoir"],
        },
        "expected_keywords": ["fantasy", "magic", "sword", "quest", "dragon"],
    },
    {
        "name": "Science-fiction dystopique",
        "answers": {
            "free_1": "Un roman de science-fiction dans un futur sombre et totalitaire",
            "free_2": "",
            "free_3": "",
            "genre": ["Dystopie", "Science-fiction"],
            "periode": "Peu importe",
            "themes": ["Liberte", "Rebellion"],
        },
        "expected_keywords": ["science fiction", "dystopia", "speculative"],
    },
    {
        "name": "Romance historique",
        "answers": {
            "free_1": "Une histoire d'amour dans un cadre historique, romantique et emouvant",
            "free_2": "",
            "free_3": "",
            "genre": ["Romance", "Historique"],
            "periode": "Avant 1950",
            "themes": ["Amour"],
        },
        "expected_keywords": ["romance", "historical"],
    },
    {
        "name": "Horreur psychologique",
        "answers": {
            "free_1": "Je veux un livre qui fait vraiment peur, avec une ambiance angoissante",
            "free_2": "",
            "free_3": "",
            "genre": ["Horreur"],
            "periode": "Peu importe",
            "themes": ["Mort", "Secret"],
        },
        "expected_keywords": ["horror", "gothic"],
    },
    {
        "name": "Policier enquete",
        "answers": {
            "free_1": "Une enquete policiere avec un detective qui doit resoudre un meurtre",
            "free_2": "",
            "free_3": "",
            "genre": ["Policier / Crime"],
            "periode": "Peu importe",
            "themes": ["Justice", "Secret"],
        },
        "expected_keywords": ["crime", "detective", "mystery", "thriller"],
    },
]


def is_relevant(book, expected_keywords):
    haystack = f"{book.genres} {book.summary}".lower()
    return any(keyword in haystack for keyword in expected_keywords)


def precision_at_k(recos, expected_keywords, k=TOP_K):
    top = recos[:k]
    if not top:
        return 0.0
    hits = sum(1 for book in top if is_relevant(book, expected_keywords))
    return hits / len(top)


def random_baseline(books, expected_keywords, k=TOP_K, trials=200, seed=42):
    rng = random.Random(seed)
    scores = []
    for _ in range(trials):
        sample = rng.sample(books, k)
        hits = sum(
            1
            for book in sample
            if any(kw in f"{book.get('genres', '')} {book.get('summary', '')}".lower() for kw in expected_keywords)
        )
        scores.append(hits / k)
    return statistics.mean(scores)


def main():
    books = load_books()
    print(f"Referentiel charge : {len(books)} livres\n")

    model_scores = []
    baseline_scores = []

    print(f"{'Profil':<28} {'Precision@5 (modele)':<22} {'Precision@5 (aleatoire)':<24} {'Gain'}")
    print("-" * 90)

    for profile in PROFILES:
        _, coverage, book_recos, _, mode = run_pipeline(profile["answers"], books)
        if not book_recos:
            print(f"{profile['name']:<28} aucun resultat (mode={mode})")
            continue

        p_model = precision_at_k(book_recos, profile["expected_keywords"])
        p_random = random_baseline(books, profile["expected_keywords"])
        gain = p_model - p_random

        model_scores.append(p_model)
        baseline_scores.append(p_random)

        print(
            f"{profile['name']:<28} {p_model:<22.2%} {p_random:<24.2%} {gain:+.2%}"
        )

    print("-" * 90)
    print(f"Moyenne modele    : {statistics.mean(model_scores):.2%}")
    print(f"Moyenne aleatoire : {statistics.mean(baseline_scores):.2%}")
    print(f"Gain moyen        : {statistics.mean(model_scores) - statistics.mean(baseline_scores):+.2%}")
    print(f"\n(Embedding mode utilise : {mode})")


if __name__ == "__main__":
    main()
