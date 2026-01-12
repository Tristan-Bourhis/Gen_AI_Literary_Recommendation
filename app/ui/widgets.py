import streamlit as st


def render_text(question):
    return st.text_area(question["label"], key=question["id"])


def render_scale(question):
    return st.slider(
        question["label"],
        question.get("min", 1),
        question.get("max", 5),
        question.get("default", 3),
        key=question["id"],
    )


def render_select(question):
    return st.selectbox(
        question["label"],
        question.get("options", []),
        key=question["id"],
    )


def render_multiselect(question):
    return st.multiselect(
        question["label"],
        question.get("options", []),
        key=question["id"],
    )


def render_question(question):
    qtype = question["type"]
    if qtype == "text":
        return render_text(question)
    if qtype == "scale":
        return render_scale(question)
    if qtype == "select":
        return render_select(question)
    if qtype == "multiselect":
        return render_multiselect(question)
    st.warning(f"Type de question inconnu: {qtype}")
    return None
