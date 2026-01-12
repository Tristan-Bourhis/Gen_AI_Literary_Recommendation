import pandas as pd
import streamlit as st

from app.services.referential_loader import load_books, load_questions
from app.ui.state import init_state


st.set_page_config(page_title="Referentiel", layout="wide")
init_state()

st.title("Referentiel")

st.subheader("Livres")
book_df = pd.DataFrame(load_books())
st.dataframe(book_df, use_container_width=True)

st.subheader("Questions")
question_df = pd.DataFrame(load_questions())
st.dataframe(question_df, use_container_width=True)
