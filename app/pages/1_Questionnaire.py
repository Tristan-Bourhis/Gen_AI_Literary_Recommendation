import streamlit as st
import json
import hashlib

# --- IMPORTS DESIGN & STATE ---
from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state

# --- IMPORTS LOGIQUE ---
from app.services.referential_loader import load_questions, load_books
from app.ui.forms import render_questionnaire
from app.services.storage import save_responses
from app.nlp.pipeline import run_pipeline

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
    uploaded_file = st.file_uploader("Fichier JSON", type=["json"], label_visibility="collapsed")
    
    if uploaded_file is not None and st.button("Charger ce profil"):
        try:
            payload = json.loads(uploaded_file.read().decode("utf-8"))
            # On récupère les réponses (format direct ou sous clé "answers")
            answers_to_load = payload.get("answers", payload)
            
            count = 0
            # Mise à jour du Session State
            for q in questions:
                q_id = q["id"]
                if q_id in answers_to_load:
                    # On force la valeur dans la mémoire de Streamlit
                    st.session_state[q_id] = answers_to_load[q_id]
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