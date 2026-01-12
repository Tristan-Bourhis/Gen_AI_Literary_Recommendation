import json

import streamlit as st

from app.services.referential_loader import load_questions
from app.services.storage import save_responses
from app.ui.forms import render_questionnaire
from app.ui.state import init_state


st.set_page_config(page_title="Questionnaire", layout="wide")
init_state()

st.title("Questionnaire de preferences de lecture")
st.caption("Complete les sections puis va dans Resultats pour l'analyse.")

questions = load_questions()

st.subheader("Importer des reponses")
uploaded_file = st.file_uploader(
    "Choisis un fichier JSON exporte precedemment",
    type=["json"],
)
if uploaded_file is not None and st.button("Importer"):
    payload = json.loads(uploaded_file.read().decode("utf-8"))
    answers = payload.get("answers", payload)
    for question in questions:
        if question["id"] in answers:
            st.session_state[question["id"]] = answers[question["id"]]
    st.session_state["answers"] = answers
    st.success("Reponses importees. Verifie puis soumets le questionnaire.")

answers, submitted = render_questionnaire(questions)

if submitted:
    st.session_state["answers"] = answers
    payload = {
        "user_id": st.session_state["user_id"],
        "answers": answers,
    }
    saved_path = save_responses(payload)
    st.success(f"Reponses enregistrees: {saved_path}. Ouvre la page Resultats.")
