import streamlit as st
import json
import os

# --- 1. IMPORTS DESIGN & STATE ---
from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state

# --- 2. CONFIGURATION ---
st.set_page_config(
    page_title="Bookscout AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. CHARGEMENT STYLE ---
init_state()
load_custom_css()
display_header()

# --- 4. LOGIQUE DE NAVIGATION ---
if "started" not in st.session_state:
    st.session_state["started"] = False

# =========================================================
# PAGE D'ACCUEIL (LANDING PAGE)
# =========================================================
if not st.session_state["started"]:
    
    # 1. HERO SECTION
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0;">
                Trouvez votre prochain <span style="color: #6BC293;">Coup de Cœur littéraire</span>
            </h1>
            <p style="font-size: 1.4rem; color: #CCCCCC; margin-top: 1rem; max-width: 800px; margin-left: auto; margin-right: auto;">
                Fini les recherches interminables. Décrivez vos envies, notre 
                <strong style="color:white;">Intelligence Artificielle</strong> vous guide vers votre prochaine lecture idéale.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 2. CALL TO ACTION
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.write("") # Espace vertical
        if st.button("🚀  Lancer l'expérience Bookscout", use_container_width=True):
            st.session_state["started"] = True
            st.switch_page("pages/1_Questionnaire.py")

    st.markdown("---")

    # 3. FEATURES (Colonnes explicatives)
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>💡 Comment ça fonctionne ?</h3>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%;">
            <h2 style="text-align: center;">🗣️</h2>
            <h4 style="text-align: center; color: #6BC293;">1. Exprimez-vous</h4>
            <p style="text-align: center; color: #ddd; font-size: 0.95rem;">
                Racontez-nous ce que vous aimez avec vos propres mots, ou laissez-vous simplement guider par nos questions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%;">
            <h2 style="text-align: center;">🧠</h2>
            <h4 style="text-align: center; color: #6BC293;">2. Analyse IA</h4>
            <p style="text-align: center; color: #ddd; font-size: 0.95rem;">
                Notre moteur SBERT analyse le sens profond de vos mots pour comprendre vos goûts littéraires.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%;">
            <h2 style="text-align: center;">✨</h2>
            <h4 style="text-align: center; color: #6BC293;">3. Découvrez</h4>
            <p style="text-align: center; color: #ddd; font-size: 0.95rem;">
                Recevez une sélection sur-mesure et une synthèse explicative générée par IA.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("") # Petit espace

    # 4. SECTION "POURQUOI" (Gardée, mais une seule fois !)
    with st.expander("🧐 Pourquoi utiliser Bookscout plutôt qu'une simple recherche ?"):
        st.markdown("""
        * **🔎 Compréhension Contextuelle :** Nous ne cherchons pas juste des mots-clés, nous comprenons *l'ambiance*.
        * **⚡ Rapidité :** Scannez des centaines de résumés en une fraction de seconde.
        * **🎯 Précision :** Un système de scoring transparent pour savoir pourquoi un livre vous est proposé.
        """)

    st.markdown("<br><br>", unsafe_allow_html=True)

# =========================================================
# REDIRECTION
# =========================================================
else:
    st.switch_page("pages/1_Questionnaire.py")