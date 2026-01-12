import uuid
import streamlit as st


STATE_KEYS = {
    "user_id": None,
    "answers": {},
    "segments": [],
    "book_recos": [],
    "similarities": None,
    "embed_mode": None,
}


def init_state():
    for key, default in STATE_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default
    if not st.session_state["user_id"]:
        st.session_state["user_id"] = str(uuid.uuid4())
