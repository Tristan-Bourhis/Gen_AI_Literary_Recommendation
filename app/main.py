import streamlit as st

from app.ui.state import init_state


st.set_page_config(page_title="Accueil", layout="wide")
init_state()

st.title("Recommandation litteraire par analyse semantique")
st.write(
    "Utilise la navigation pour remplir le questionnaire puis consulter les recommandations."
)

col1, col2 = st.columns(2)
with col1:
    st.info("Commence par la page Questionnaire.")
with col2:
    st.info("Consulte Resultats pour le score et les recommandations.")
