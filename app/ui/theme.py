import streamlit as st
import base64
import os

def load_custom_css():
    """
    CSS Global : Logo, Titres, Cartes et Progress Bar.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');

        /* 1. TYPOGRAPHIE GLOBALE */
        html, body, [class*="css"], .stMarkdown, p {
            font-family: 'Outfit', sans-serif;
            color: #FFFFFF !important;
        }

        /* 2. TITRE PRINCIPAL (Résultats) */
        .result-title {
            font-size: 3rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #ffffff, #6BC293);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .result-subtitle {
            font-size: 1.2rem;
            color: #cccccc !important;
            text-align: center;
            margin-bottom: 40px;
            font-weight: 300;
        }

        /* 3. DESIGN DES CARTES (Correction et Style) */
        .book-card {
            background-color: #1A1B1E;
            border: 1px solid #333;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            /* Bordure verte à gauche */
            border-left: 6px solid #6BC293;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            height: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(107, 194, 147, 0.2);
            border-color: #6BC293;
        }

        .book-title { 
            color: #FFFFFF; 
            font-weight: 700; 
            font-size: 1.3rem; 
            margin-bottom: 5px;
            line-height: 1.2;
        }
        
        .book-author {
            color: #AAAAAA;
            font-size: 0.95rem;
            font-style: italic;
            margin-bottom: 15px;
        }

        /* Badge Score */
        .score-badge {
            background-color: #6BC293;
            color: #000;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.85rem;
            display: inline-block;
        }

        /* 4. BARRE DE PROGRESSION (Customisation couleur verte) */
        .stProgress > div > div > div > div {
            background-color: #6BC293;
        }

        /* 5. LOGO */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 0rem;
        }
        .logo-img { max-width: 300px; width: 100%; height: auto; }
        
        /* Cacher la sidebar */
        section[data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_header():
    if os.path.exists("Bookscout.png"):
        img_b64 = get_base64_image("Bookscout.png")
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{img_b64}" class="logo-img" alt="Bookscout Logo" style="width: 300px; max-width: 300px;">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #6BC293;'>Bookscout</h2>", unsafe_allow_html=True)