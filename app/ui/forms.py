import streamlit as st
from app.ui.widgets import render_question

def _display_section_header(title, icon, subtitle):
    """Affiche un en-tête de section stylisé."""
    st.markdown(f"""
        <div style="
            background-color: #1E1E1E; 
            border-left: 5px solid #6BC293; 
            padding: 15px 20px; 
            border-radius: 8px; 
            margin-top: 30px; 
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        ">
            <h3 style="margin: 0; color: #FFFFFF; font-size: 1.4rem;">
                {icon} &nbsp; {title}
            </h3>
            <p style="margin: 5px 0 0 0; color: #AAAAAA; font-size: 0.95rem;">
                {subtitle}
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_questionnaire(questions):
    """
    Génère le formulaire en mode 'Tout-Terrain'.
    Affiche ABSOLUMENT TOUTES les questions, quoi qu'il arrive.
    """
    answers = {}
    submitted = False
    
    # Sécurité : si la liste est vide, on prévient
    if not questions:
        st.error("⚠️ Aucune question trouvée. Vérifiez le fichier questions.json.")
        return {}, False

    with st.form("user_preferences_form"):
        
        # --- GROUPE 1 : LES QUESTIONS TEXTE ---
        # On essaie de trouver les questions ouvertes pour les mettre en intro
        text_questions = []
        other_questions = []

        for q in questions:
            # On normalise le type pour éviter les erreurs de majuscules
            q_type = q.get("type", "text").lower().strip()
            
            # Si c'est du texte, on met de côté pour l'intro
            if q_type in ["text", "text_area", "textarea", "free", "input"]:
                text_questions.append(q)
            else:
                other_questions.append(q)
        
        # 1. Affichage des questions Texte (s'il y en a)
        if text_questions:
            _display_section_header(
                "Vos envies du moment", 
                "✍️", 
                "Décrivez ce que vous cherchez."
            )
            for q in text_questions:
                answers[q["id"]] = render_question(q)
                st.write("") # Espace

        # 2. Affichage de TOUT LE RESTE (Likert, Choix, etc.)
        if other_questions:
            _display_section_header(
                "Vos Critères", 
                "🎚️", 
                "Affinez votre recherche."
            )
            
            for q in other_questions:
                # On affiche la question
                answers[q["id"]] = render_question(q)
                
                # Petit espace entre chaque question pour aérer
                st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- BOUTON DE VALIDATION ---
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button(
                "✨ Lancer l'analyse IA", 
                use_container_width=True
            )

    return answers, submitted