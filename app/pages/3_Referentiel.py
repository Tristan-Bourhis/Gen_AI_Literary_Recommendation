import streamlit as st
import pandas as pd

# --- 1. IMPORTS DESIGN & STATE ---
from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state

# --- 2. IMPORTS DATA (Indispensables !) ---
from app.services.referential_loader import load_books, load_questions

# --- 3. CONFIGURATION ---
st.set_page_config(
    page_title="Référentiel - Bookscout",
    page_icon="📚",
    layout="wide"
)

# --- 4. CHARGEMENT DU STYLE ---
init_state()
load_custom_css()
display_header()

# --- 5. CONTENU DE LA PAGE ---

st.title("📂 Données du Référentiel")
st.markdown("Consultation des sources, des livres et de la structure du questionnaire utilisés par l'IA.")

# --- SECTION 1 : LIVRES ---
st.header("📚 Base de données Livres")

books = load_books()

if not books:
    st.error("Aucun livre trouvé dans le référentiel.")
else:
    # Conversion robuste en DataFrame (compatible objets ou dicts)
    data = [b if isinstance(b, dict) else b.__dict__ for b in books]
    book_df = pd.DataFrame(data)

    # Affichage de statistiques (KPIs) pour le jury
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ouvrages", len(book_df))
    col2.metric("Auteurs Uniques", book_df["author"].nunique() if "author" in book_df.columns else 0)
    col3.metric("Genres", book_df["genres"].nunique() if "genres" in book_df.columns else 0)

    st.markdown("### Aperçu des données")
    
    # Configuration des colonnes pour un affichage propre
    st.dataframe(
        book_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "summary": st.column_config.TextColumn("Résumé", width="large"),
            "title": st.column_config.TextColumn("Titre", width="medium"),
            "author": "Auteur",
            "publication_year": st.column_config.NumberColumn("Année", format="%d"),
            "embedding": None, # On cache les vecteurs illisibles
            "book_id": None
        },
        height=500
    )

st.markdown("---")

# --- SECTION 2 : QUESTIONS ---
st.header("❓ Structure du Questionnaire")

questions = load_questions()

if not questions:
    st.warning("Aucune question chargée.")
else:
    question_df = pd.DataFrame(questions)
    
    st.caption(f"Le système utilise {len(question_df)} points de données pour profiler l'utilisateur.")
    
    st.dataframe(
        question_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.TextColumn("ID Technique", width="small"),
            "text": st.column_config.TextColumn("Question posée", width="large"),
            "type": "Type"
        }
    )