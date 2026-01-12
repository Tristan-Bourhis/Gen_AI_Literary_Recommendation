import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import MODEL_NAME


class EmbeddingModel:
    def __init__(self, model=None, mode="tfidf"):
        self.model = model
        self.mode = mode
        self.vectorizer = None

    def encode(self, texts, fit_texts=None):
        if not texts:
            return np.empty((0, 1))
        if self.mode == "sbert":
            return self.model.encode(texts)
        if fit_texts is None:
            fit_texts = texts
        self.vectorizer = TfidfVectorizer()
        matrix = self.vectorizer.fit_transform(fit_texts).toarray()
        if fit_texts is texts:
            return matrix
        return self.vectorizer.transform(texts).toarray()


def load_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer

        return EmbeddingModel(SentenceTransformer(MODEL_NAME), "sbert")
    except Exception:
        return EmbeddingModel(None, "tfidf")
