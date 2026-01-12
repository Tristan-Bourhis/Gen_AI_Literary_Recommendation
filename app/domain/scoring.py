def compute_coverage(similarities, top_k=5):
    if not similarities:
        return 0.0
    top = sorted(similarities, reverse=True)[:top_k]
    return (sum(top) / len(top)) * 100.0 if top else 0.0
