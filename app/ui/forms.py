import streamlit as st

from app.ui.widgets import render_question


SECTION_TITLES = {
    "A": "Section A - Texte libre",
    "B": "Section B - Echelle (1 a 5)",
    "C": "Section C - Questions guidees",
}


def render_questionnaire(questions):
    submitted = False
    answers = {}
    with st.form("questionnaire"):
        for section in ["A", "B", "C"]:
            st.subheader(SECTION_TITLES.get(section, section))
            for question in [q for q in questions if q["section"] == section]:
                answers[question["id"]] = render_question(question)
        submitted = st.form_submit_button("Analyser")
    return answers, submitted
