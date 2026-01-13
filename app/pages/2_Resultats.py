import os

import streamlit as st

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

from app.nlp.pipeline import run_pipeline
from app.services.genai import build_synthesis_prompt, generate_synthesis
from app.services.referential_loader import load_books
from app.ui.state import init_state
from app.ui.theme import apply_book_theme
from app.ui.viz import show_books, show_coverage, show_similarity, show_synthesis


st.set_page_config(page_title="Resultats", layout="wide")
init_state()
apply_book_theme()

st.title("Resultats")

answers = st.session_state.get("answers")
if not answers:
    st.warning("Aucune reponse disponible. Remplis le questionnaire.")
    st.stop()

books = load_books()
segments, coverage, book_recos, similarities, mode = run_pipeline(answers, books)

if coverage is None:
    st.warning("Reponses insuffisantes pour l'analyse.")
    st.stop()

st.session_state["segments"] = segments
st.session_state["book_recos"] = book_recos
st.session_state["similarities"] = similarities
st.session_state["embed_mode"] = mode

st.subheader("Score de couverture")
show_coverage(coverage, mode)

st.subheader("Livres suggeres")
show_books(book_recos)

st.subheader("Carte de similarite")
labels = [label for label, text in segments if text]
book_titles = [book["title"] for book in books][:10]
if similarities is not None:
    show_similarity(similarities[:, : len(book_titles)], labels, book_titles)

st.subheader("Synthese GenAI")
if load_dotenv:
    load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    st.info("Ajoute GEMINI_API_KEY dans l'environnement pour activer la synthese.")
else:
    if st.button("Generer la synthese"):
        prompt = build_synthesis_prompt(answers, book_recos)
        text, cached = generate_synthesis(prompt, api_key)
        show_synthesis(text, cached=cached)
