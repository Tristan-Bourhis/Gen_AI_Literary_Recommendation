import streamlit as st

# --- IMPORTS ---
from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state
from app.ui.viz import (
    show_top3_cards, 
    show_reader_radar, 
    show_embedding_scatter,
    show_genre_bars,
    show_similarity_heatmap,
    show_books, 
    show_synthesis
)
from app.services.genai import generate_synthesis

# 1. CONFIGURATION
st.set_page_config(page_title="Résultats - Bookscout", page_icon="🔮", layout="wide", initial_sidebar_state="collapsed")

# 2. STYLE & HEADER
init_state()
load_custom_css()
display_header()

st.progress(100)
st.caption("Analyse terminée avec succès ✅")
st.markdown("<br>", unsafe_allow_html=True)

# 3. VERIFICATION
if "book_recos" not in st.session_state or not st.session_state["book_recos"]:
    st.warning("Aucun résultat.")
    if st.button("Retour"): st.switch_page("pages/1_Questionnaire.py")
    st.stop()

# DATA
book_recos = st.session_state["book_recos"]
answers = st.session_state.get("answers", {})

# ---------------------------------------------------------
# A. RÉSULTATS PRINCIPAUX (CARTES)
# ---------------------------------------------------------
st.markdown('<div class="result-title">Vos Pépites Littéraires</div>', unsafe_allow_html=True)
st.markdown('<div class="result-subtitle">Voici la sélection issue de notre analyse sémantique.</div>', unsafe_allow_html=True)

show_top3_cards(book_recos, [], [], book_recos)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# B. TABLEAU DE BORD (4 VISUELS BIEN SÉPARÉS)
# ---------------------------------------------------------
st.markdown("### 📊 Tableau de Bord Analytique")
st.caption("Indicateurs clés de la recommandation.")
st.write("") 

# --- LIGNE 1 ---
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>1. Profil Radar</h5>", unsafe_allow_html=True)
        show_reader_radar(answers)
        st.caption("Forme de vos préférences déclarées.")

with col2:
    with st.container(border=True):
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>2. Carte Sémantique</h5>", unsafe_allow_html=True)
        show_embedding_scatter(book_recos)
        st.caption("Positionnement : Ambiance vs Densité.")

st.markdown("<br>", unsafe_allow_html=True)

# --- LIGNE 2 ---
col3, col4 = st.columns(2, gap="large")

with col3:
    with st.container(border=True):
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>3. Top Genres</h5>", unsafe_allow_html=True)
        show_genre_bars(book_recos)
        st.caption("Les styles dominants (sans vide).")

with col4:
    with st.container(border=True):
        # Changement de titre ici
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>4. Analyse des Critères</h5>", unsafe_allow_html=True)
        show_similarity_heatmap(book_recos)
        st.caption("Correspondance : Livres vs Critères clés.")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# C. SYNTHESE IA
# ---------------------------------------------------------
st.markdown("### 🧠 L'Explication de l'IA")

if "synthesis_text" in st.session_state:
    show_synthesis(st.session_state["synthesis_text"], cached=True)
else:
    st.info("💡 Cliquez ci-dessous pour obtenir une analyse détaillée.")
    if st.button("✨ Générer l'explication (IA)", type="primary"):
        with st.spinner("Rédaction en cours..."):
            try:
                synthesis = generate_synthesis(str(answers), book_recos[:3])
                st.session_state["synthesis_text"] = synthesis
                st.rerun()
            except:
                st.error("Service IA indisponible.")

# LISTE BRUTE
with st.expander("📚 Voir les données brutes"):
    show_books(book_recos)

st.markdown("<br><br>", unsafe_allow_html=True)
c_fin_1, c_fin_2, c_fin_3 = st.columns([1, 1, 1])
with c_fin_2:
    if st.button("🔄 Nouvelle Recherche", use_container_width=True):
        st.switch_page("pages/1_Questionnaire.py")