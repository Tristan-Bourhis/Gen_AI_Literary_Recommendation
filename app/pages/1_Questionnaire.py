import streamlit as st
import json
import hashlib
import re
import unicodedata

from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state

from app.services.referential_loader import load_questions, load_books
from app.ui.forms import render_questionnaire
from app.services.storage import save_responses
from app.nlp.pipeline import run_pipeline

def _normalize_key(text):
    if not text:
        return ""
    value = unicodedata.normalize("NFKD", str(text))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return " ".join(value.split())

def _coerce_answers_payload(payload):
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        out = {}
        for item in payload:
            if not isinstance(item, dict):
                continue
            if "id" in item and "value" in item:
                out[item["id"]] = item["value"]
            elif "key" in item and "value" in item:
                out[item["key"]] = item["value"]
        return out
    return {}

def _build_question_key_map(questions):
    mapping = {}
    for q in questions:
        q_id = q.get("id")
        if not q_id:
            continue
        q_text = q.get("text") or q.get("label") or ""
        legacy_key = None
        if q_text:
            legacy_id = hashlib.md5(q_text.encode("utf-8")).hexdigest()[:10]
            legacy_key = f"q_{legacy_id}"
        for key in [q_id, legacy_key, q_text, _normalize_key(q_text)]:
            if key:
                mapping[str(key)] = q_id
    return mapping

def _coerce_answer_value(question, value):
    q_type = (question.get("type") or "text").lower().strip()
    if q_type in ["likert", "slider", "scale"]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return value
    if q_type in ["multiselect", "multi"]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            parts = re.split(r"[;|,]", value)
            return [item.strip() for item in parts if item.strip()]
        return []
    if q_type in ["select", "dropdown", "radio", "choice"]:
        if isinstance(value, str):
            return value
        return str(value)
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)

# 1. CONFIGURATION
st.set_page_config(page_title="Profil - Bookscout", page_icon="📝", layout="wide")

# 2. CHARGEMENT STYLE
init_state()
load_custom_css()
display_header()

# 3. BARRE DE PROGRESSION & INTRO
st.progress(50)
st.caption("Étape 1 sur 2 : Définition du profil")

st.title("🎯 Ciblons vos attentes")
st.markdown("""
    Pour que l'IA puisse trouver **LE** livre parfait, elle a besoin de vous connaître un peu. 
    Pas de stress, il n'y a pas de mauvaises réponses !
""")

# =========================================================
# CHARGEMENT ET STABILISATION DES QUESTIONS
# =========================================================
questions = load_questions()

# 🔥 PATCH DE STABILITÉ : On s'assure que chaque question a un ID stable.
# Cela permet de recharger le fichier JSON sans que les liens ne soient brisés.
for i, q in enumerate(questions):
    if "id" not in q or not q["id"]:
        # On crée un ID unique basé sur le texte de la question (MD5)
        # Comme le texte ne change pas, l'ID sera toujours le même.
        unique_str = q.get("text", f"question_{i}").encode("utf-8")
        stable_id = hashlib.md5(unique_str).hexdigest()[:10]
        q["id"] = f"q_{stable_id}"

# =========================================================
# ZONE D'IMPORT (CHARGER UN PROFIL)
# =========================================================
with st.expander("📂 Vous avez déjà un fichier de profil ? (Optionnel)"):
    st.caption("Glissez ici le fichier JSON que vous avez sauvegardé lors d'un test précédent.")
    uploaded_file = st.file_uploader("Fichier JSON", type=["json"], label_visibility="collapsed", key="profile_uploader")
    
    if uploaded_file is not None and st.button("Charger ce profil"):
        try:
            payload = json.loads(uploaded_file.read().decode("utf-8"))
            # Load answers from either root or 'answers'
            raw_answers = payload.get("answers", payload)
            answers_to_load = _coerce_answers_payload(raw_answers)

            count = 0
            q_by_id = {q["id"]: q for q in questions}
            key_to_id = _build_question_key_map(questions)
            for key, value in answers_to_load.items():
                q_id = key_to_id.get(key)
                if q_id is None and isinstance(key, str):
                    q_id = key_to_id.get(_normalize_key(key))
                if q_id:
                    st.session_state[q_id] = _coerce_answer_value(q_by_id.get(q_id, {}), value)
                    count += 1

            # On stocke aussi l'objet global
            st.session_state["answers"] = answers_to_load
            
            if count > 0:
                st.success(f"Succès ! {count} réponses ont été chargées. Le formulaire ci-dessous est à jour.")
                st.rerun() # INDISPENSABLE : Relance la page pour afficher les valeurs
            else:
                st.warning("Le fichier a été lu mais aucune réponse ne correspond aux questions actuelles (les IDs ont peut-être changé).")
                
        except Exception as e:
            st.error(f"Erreur de lecture du fichier : {e}")

# =========================================================
# AFFICHAGE DU FORMULAIRE
# =========================================================
# Les widgets vont maintenant lire st.session_state et afficher vos valeurs
answers, submitted = render_questionnaire(questions)

# =========================================================
# ZONE D'EXPORT (SAUVEGARDER)
# =========================================================
json_export = json.dumps({"answers": answers}, indent=4, ensure_ascii=False)

col_ex_1, col_ex_2 = st.columns([3, 1])
with col_ex_2:
    st.download_button(
        label="💾 Sauvegarder ce profil (JSON)",
        data=json_export,
        file_name="mon_profil_bookscout.json",
        mime="application/json",
        help="Sauvegardez vos réponses pour plus tard."
    )

# =========================================================
# TRAITEMENT APRES SOUMISSION
# =========================================================
if submitted:
    # Sauvegarde en session
    st.session_state["answers"] = answers
    payload = {
        "user_id": st.session_state.get("user_id", "guest"),
        "answers": answers,
    }
    save_responses(payload)
    
    # Lancement Pipeline
    with st.spinner("🧠 Nos algorithmes lisent des centaines de résumés pour vous..."):
        try:
            books = load_books()
            segments, coverage, book_recos, similarities, mode = run_pipeline(answers, books)
            
            # Stockage des résultats
            st.session_state["segments"] = segments
            st.session_state["book_recos"] = book_recos
            st.session_state["similarities"] = similarities
            st.session_state["embed_mode"] = mode
            st.session_state["coverage"] = coverage

            st.success("Analyse terminée ! Téléportation vers les résultats... 🚀")
            st.switch_page("pages/2_Resultats.py")
            
        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'analyse : {e}")