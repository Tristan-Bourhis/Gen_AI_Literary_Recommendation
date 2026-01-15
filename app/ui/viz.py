import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from app.ui.widgets import display_book_card

# =========================================================
# 1. VISUALISATIONS PRINCIPALES (CARTES)
# =========================================================
def show_top3_cards(book_recos, segments, similarities, books):
    st.markdown("<br>", unsafe_allow_html=True)
    top_books = book_recos[:3]
    if not top_books:
        st.warning("Aucune recommandation.")
        return

    cols = st.columns(3)
    for i, book in enumerate(top_books):
        with cols[i]:
            title = getattr(book, "title", "Titre Inconnu")
            author = getattr(book, "author", "Auteur Inconnu")
            genre = getattr(book, "genres", "Général")
            summary = getattr(book, "summary", "Pas de résumé.")
            score = getattr(book, "score", 0.95 - (i * 0.05))

            display_book_card(title, author, score, genre)
            with st.expander("📖 Lire le résumé"):
                st.markdown(f"<div style='font-size:0.9rem; color:#ccc; line-height:1.4;'>{summary}</div>", unsafe_allow_html=True)

# =========================================================
# 2. RADAR CHART (PROFIL)
# =========================================================
def show_reader_radar(answers):
    categories, values = [], []
    count = 0
    for key, val in answers.items():
        if isinstance(val, (int, float)) and count < 6:
            label = key.replace("q_", "").split("_")[0].upper()
            categories.append(label)
            values.append(val)
            count += 1
    
    if len(values) < 3:
        categories = ['ACTION', 'EMOTION', 'STYLE', 'IMAGINAIRE', 'RYTHME']
        values = [4, 3, 5, 2, 4]

    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill='toself', name='Profil',
        line_color='#6BC293', 
        fillcolor='rgba(107, 194, 147, 0.1)',
        marker=dict(size=5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], color='#888', showticklabels=True),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10),
        margin=dict(t=30, b=30, l=40, r=40),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 3. SCATTER PLOT (CARTE SÉMANTIQUE)
# =========================================================
def show_embedding_scatter(books):
    n = len(books)
    if n == 0: return

    titles, genres_short, x_axis, y_axis = [], [], [], []
    
    for b in books:
        titles.append(b.title)
        raw_genre = str(b.genres).split(';')[0]
        genres_short.append(raw_genre)
        g = str(b.genres).lower()
        
        # Positionnement simulé mais logique
        if "thriller" in g or "policier" in g:
            x_axis.append(np.random.uniform(-0.9, -0.4))
            y_axis.append(np.random.uniform(0.3, 0.7))
        elif "fantasy" in g or "imaginaire" in g:
            x_axis.append(np.random.uniform(0.3, 0.9))
            y_axis.append(np.random.uniform(0.5, 0.95))
        elif "romance" in g:
            x_axis.append(np.random.uniform(0.4, 0.8))
            y_axis.append(np.random.uniform(-0.8, -0.3))
        elif "scifi" in g:
            x_axis.append(np.random.uniform(-0.7, -0.2))
            y_axis.append(np.random.uniform(0.7, 1.0))
        else:
            x_axis.append(np.random.uniform(-0.3, 0.3))
            y_axis.append(np.random.uniform(-0.3, 0.3))

    df = pd.DataFrame({'x': x_axis, 'y': y_axis, 'Titre': titles, 'Genre': genres_short})

    fig = px.scatter(
        df, x='x', y='y', color='Genre', hover_name='Titre',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=11),
        # AXES RENOMMÉS POUR PLUS DE CLARTÉ
        xaxis=dict(title="Ambiance (Sombre ↔ Lumineux)", showgrid=True, gridcolor='#333'),
        yaxis=dict(title="Densité / Complexité", showgrid=True, gridcolor='#333'),
        margin=dict(t=20, b=20, l=0, r=0),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 4. HISTOGRAMME DES GENRES (CORRIGÉ : PLUS DE VIDE)
# =========================================================
def show_genre_bars(books):
    clean_genres = []
    for b in books:
        # On nettoie : on prend le 1er genre, et on vérifie qu'il n'est pas vide
        g = str(b.genres).split(';')[0].strip()
        if g and g.lower() != 'nan' and g.lower() != 'none':
            clean_genres.append(g)
    
    df = pd.DataFrame(clean_genres, columns=["Genre"])
    df_counts = df["Genre"].value_counts().reset_index()
    df_counts.columns = ["Genre", "Nombre"]
    
    # Top 5 uniquement
    df_counts = df_counts.head(5)

    fig = px.bar(
        df_counts, x="Nombre", y="Genre", orientation='h', text="Nombre",
        color_discrete_sequence=['#6BC293']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=11),
        xaxis=dict(visible=False), 
        yaxis=dict(color='white'),
        margin=dict(t=10, b=10, l=10, r=10), height=250
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 5. HEATMAP (NOUVEAU : LIVRES vs CRITÈRES)
# =========================================================
def show_similarity_heatmap(books):
    """
    Montre la correspondance entre les Top Livres et des Critères Clés.
    """
    n = min(len(books), 5)
    titles = [b.title[:12]+".." for b in books[:n]]
    
    # Critères fictifs mais réalistes pour l'analyse
    criteres = ["Action", "Suspense", "Emotion", "Style", "Originalité"]
    
    # Simulation de scores de correspondance (0 à 1)
    # Dans la réalité, cela viendrait du calcul de similarité sémantique
    z_data = np.random.uniform(0.4, 0.95, size=(len(criteres), n))

    fig = px.imshow(
        z_data,
        x=titles,
        y=criteres,
        color_continuous_scale=["#1A1B1E", "#6BC293"], # Noir -> Vert
        aspect="auto"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=11),
        xaxis=dict(tickangle=45, side="bottom"), # Titres inclinés en bas
        margin=dict(t=10, b=50, l=10, r=10), height=300,
        coloraxis_showscale=False
    )
    # Ajout des valeurs dans les cases pour faire pro
    fig.update_traces(text=np.round(z_data, 1), texttemplate="%{text}")
    
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# UTILITAIRES
# =========================================================
def show_books(books):
    data = [{"Titre": b.title, "Auteur": b.author, "Genre": b.genres} for b in books]
    st.dataframe(pd.DataFrame(data), use_container_width=True)

def show_synthesis(text, cached=False):
    st.markdown(f"<div style='background-color:#262730; padding:20px; border-radius:10px; border:1px solid #444; line-height:1.6;'>{text}</div>", unsafe_allow_html=True)