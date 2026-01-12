import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_matrix(a, b):
    if a.size == 0 or b.size == 0:
        return np.empty((0, 0))
    return cosine_similarity(a, b)


def top_k(similarities, labels, k):
    if similarities.size == 0:
        return []
    scores = similarities.mean(axis=0)
    pairs = list(zip(labels, scores))
    pairs.sort(key=lambda item: item[1], reverse=True)
    return pairs[:k]
