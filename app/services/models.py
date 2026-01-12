import streamlit as st

from app.nlp.embeddings import load_embedding_model


@st.cache_resource(show_spinner=False)
def get_embedding_model():
    return load_embedding_model()
