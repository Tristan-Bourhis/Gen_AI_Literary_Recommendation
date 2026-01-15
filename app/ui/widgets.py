import json
import streamlit as st

# ==========================================
# 1. CARTE DE LIVRE (Correction HTML)
# ==========================================
def display_book_card(title, author, score, genre):
    """
    Affiche une carte propre sans afficher le code HTML brut.
    """
    match_percent = int(score * 100)
    
    # HTML Simplifié et Propre
    html_code = f"""
    <div class="book-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div style="flex:1;">
                <div class="book-title">{title}</div>
                <div class="book-author">par {author}</div>
            </div>
            <div class="score-badge">
                {match_percent}% Match
            </div>
        </div>
        <div style="margin-top:10px; border-top:1px solid #333; padding-top:10px;">
            <span style="color:#6BC293; font-weight:600; font-size:0.85rem; text-transform:uppercase;">
                🏷️ {genre}
            </span>
        </div>
    </div>
    """
    # C'est cette ligne qui empêche le code de s'afficher en texte
    st.markdown(html_code, unsafe_allow_html=True)


# ==========================================
# 2. ELEMENTS DU FORMULAIRE (Inchangé mais nécessaire)
# ==========================================
def render_question(question):
    q_type = question.get("type", "text").lower().strip()
    label = question.get("label") or question.get("text") or "Question"
    qid = question.get("id", str(hash(label)))
    options = question.get("options", [])
    current_value = st.session_state.get(qid)

    if q_type in ["likert", "slider", "scale"]:
        default_val = int(current_value) if current_value else 3
        return st.slider(label, 1, 5, default_val, key=qid)
    elif q_type in ["text_area", "text", "textarea"]:
        if current_value is None:
            val = ""
        elif isinstance(current_value, str):
            val = current_value
        else:
            val = json.dumps(current_value, ensure_ascii=False)
            st.session_state[qid] = val
        return st.text_area(label, value=val, height=100, key=qid)
    elif q_type in ["select", "dropdown"]:
        idx = options.index(current_value) if current_value in options else 0
        return st.selectbox(label, options, index=idx, key=qid)
    elif q_type in ["multiselect", "multi"]:
        default_vals = current_value if isinstance(current_value, list) else []
        return st.multiselect(label, options, default=default_vals, key=qid)
    elif q_type in ["radio", "choice"]:
        idx = options.index(current_value) if current_value in options else 0
        return st.radio(label, options, index=idx, key=qid)
    else:
        if current_value is None:
            val = ""
        elif isinstance(current_value, str):
            val = current_value
        else:
            val = json.dumps(current_value, ensure_ascii=False)
            st.session_state[qid] = val
        return st.text_input(label, value=val, key=qid)
