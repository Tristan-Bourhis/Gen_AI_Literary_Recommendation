import re


def normalize(text):
    if not text:
        return ""
    lowered = text.strip().lower()
    return re.sub(r"\s+", " ", lowered)


def concat_segments(segments):
    return " ".join([normalize(text) for _, text in segments if text])
