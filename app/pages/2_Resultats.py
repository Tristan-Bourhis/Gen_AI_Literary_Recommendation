import streamlit as st
import pandas as pd

# --- IMPORTS ---
from app.ui.theme import load_custom_css, display_header
from app.ui.state import init_state
from app.ui.widgets import display_book_card
from app.ui.viz import (
    show_top3_cards, 
    show_reader_radar, 
    show_embedding_scatter,
    show_genre_bars,
    show_similarity_heatmap,
    show_books, 
    show_synthesis
)
from app.services.genai import build_synthesis_prompt, generate_synthesis

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


def _normalize_tokens(value):
    if not value:
        return []
    if isinstance(value, list):
        return [item.strip().lower() for item in value if str(item).strip()]
    return [item.strip().lower() for item in str(value).replace("|", ";").split(";") if item.strip()]


def _extract_genres(books):
    genres = set()
    for book in books:
        for genre in _normalize_tokens(getattr(book, "genres", "")):
            if genre:
                genres.add(genre)
    return sorted(genres)


def _extract_periods(books):
    periods = set()
    for book in books:
        period = str(getattr(book, "period", "")).strip()
        if period:
            periods.add(period)
    return sorted(periods)


def _build_reco_dataframe(books):
    rows = []
    for book in books:
        rows.append(
            {
                "Titre": book.title,
                "Auteur": book.author,
                "Genre": book.genres,
                "Periode": book.period,
                "Annee": book.publication_year or book.publication_year_raw,
                "Score": round(float(book.score), 3),
            }
        )
    return pd.DataFrame(rows)

# ---------------------------------------------------------
# A. RÉSULTATS PRINCIPAUX (CARTES)
# ---------------------------------------------------------
st.markdown('<div class="result-title">Vos Pépites Littéraires</div>', unsafe_allow_html=True)
st.markdown('<div class="result-subtitle">Voici la sélection issue de notre analyse sémantique.</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### Filtres")
    st.caption("Ajustez les critÇùres pour explorer diffÇ¸rentes recommandations.")
    col_f1, col_f2 = st.columns(2, gap="large")
    with col_f1:
        genre_options = _extract_genres(book_recos)
        period_options = _extract_periods(book_recos)
        selected_genres = st.multiselect(
            "Genres",
            options=genre_options,
            help="Filtrer les recommandations par genres (multi-sÇ¸lection).",
        )
        selected_periods = st.multiselect(
            "PÇ¸riodes",
            options=period_options,
            help="Filtrer selon la pÇ¸riode littÇ¸raire (ex: 19e, 20e).",
        )
    with col_f2:
        scores = [float(b.score) for b in book_recos] if book_recos else [0.0]
        raw_min = float(min(scores)) if scores else 0.0
        raw_max = float(max(scores)) if scores else 1.0
        slider_min = raw_min if raw_min < raw_max else 0.0
        slider_max = raw_max if raw_min < raw_max else 1.0
        min_score = st.slider(
            "Score minimum",
            min_value=round(slider_min, 2),
            max_value=round(slider_max, 2),
            value=round(raw_min, 2),
            step=0.01,
            help="Ne garder que les livres avec un score au-dessus de ce seuil.",
        )
        base_top_k = [5, 10, 20, 50]
        top_k_options = sorted({opt for opt in base_top_k if opt <= len(book_recos)} | {len(book_recos)})
        default_top_k = 10 if 10 in top_k_options else top_k_options[0]
        top_k = st.selectbox(
            "Top-K",
            options=top_k_options,
            index=top_k_options.index(default_top_k),
            help="Limiter le nombre de recommandations affichÇ¸es.",
        )

selected_genres_norm = {g.lower() for g in selected_genres}
selected_periods_norm = {p.lower() for p in selected_periods}
filtered_recos = []
for book in book_recos:
    book_genres = set(_normalize_tokens(getattr(book, "genres", "")))
    book_period = str(getattr(book, "period", "")).strip().lower()
    if selected_genres_norm and not book_genres.intersection(selected_genres_norm):
        continue
    if selected_periods_norm and book_period not in selected_periods_norm:
        continue
    if float(book.score) < float(min_score):
        continue
    filtered_recos.append(book)
filtered_recos = filtered_recos[: min(top_k, len(filtered_recos))]

if not filtered_recos:
    st.warning("Aucun livre ne correspond aux filtres actuels. Essayez d'assouplir les critÇùres.")
else:
    st.caption(f"{len(filtered_recos)} recommandation(s) affichÇ¸e(s) aprÇùs filtrage.")

show_top3_cards(filtered_recos, [], [], filtered_recos)

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
        st.caption("Ce graphique montre la forme globale de vos préférences déclarées.")

with col2:
    with st.container(border=True):
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>2. Carte Sémantique</h5>", unsafe_allow_html=True)
        if filtered_recos:
            show_embedding_scatter(filtered_recos)
            st.caption("Ce graphique montre le positionnement des livres (Ambiance vs Densité).")
        else:
            st.info("Aucune recommandation filtrée pour afficher la carte sémantique.")

st.markdown("<br>", unsafe_allow_html=True)

# --- LIGNE 2 ---
col3, col4 = st.columns(2, gap="large")

with col3:
    with st.container(border=True):
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>3. Top Genres</h5>", unsafe_allow_html=True)
        if filtered_recos:
            show_genre_bars(filtered_recos)
            st.caption("Ce graphique montre les genres dominants dans la sélection filtrée.")
        else:
            st.info("Aucune recommandation filtrée pour afficher les genres.")

with col4:
    with st.container(border=True):
        # Changement de titre ici
        st.markdown("<h5 style='text-align:center; color:#6BC293; margin-bottom:15px;'>4. Analyse des Critères</h5>", unsafe_allow_html=True)
        if filtered_recos:
            show_similarity_heatmap(filtered_recos)
            st.caption("Ce graphique montre la correspondance Livres vs Critères clés.")
        else:
            st.info("Aucune recommandation filtrée pour afficher la heatmap.")

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
                synthesis_books = filtered_recos if filtered_recos else book_recos
                prompt = build_synthesis_prompt(answers, synthesis_books)
                synthesis, _cached = generate_synthesis(prompt)
                st.session_state["synthesis_text"] = synthesis
                st.rerun()
            except Exception as exc:
                st.error("Service IA indisponible.")
                st.caption(f"Erreur IA: {exc}")

# ---------------------------------------------------------
# D. DETAILS DES RECOMMANDATIONS
# ---------------------------------------------------------
st.markdown("### 📚 Détails des recommandations")
st.caption("Ouvrez un livre pour comprendre le score et les correspondances.")

detail_cols = st.columns(2, gap="large")
for idx, book in enumerate(filtered_recos):
    with detail_cols[idx % 2]:
        display_book_card(book.title, book.author, book.score, book.genres)
        with st.expander("Voir détails"):
            breakdown = getattr(book, "score_breakdown", None) or {}
            matches = getattr(book, "segment_matches", None) or []

            st.markdown("**Raison du score**")
            if breakdown:
                st.markdown(
                    "- Similarité sémantique : "
                    f"{breakdown.get('base_similarity', 0.0):.2f}"
                )
                st.markdown(
                    "- Bonus genre : "
                    f"{breakdown.get('genre_bonus', 0.0):.2f}"
                )
                st.markdown(
                    "- Bonus période : "
                    f"{breakdown.get('period_bonus', 0.0):.2f}"
                )
                st.markdown(
                    "- Bonus auteur : "
                    f"{breakdown.get('author_bonus', 0.0):.2f}"
                )
                st.markdown(
                    "- Bonus thèmes : "
                    f"{breakdown.get('themes_bonus', 0.0):.2f}"
                )
                st.markdown(
                    "- Pénalités (à éviter) : "
                    f"{breakdown.get('avoid_penalty', 0.0):.2f}"
                )
                st.markdown(
                    "- Score final : "
                    f"{breakdown.get('combined_score', book.score):.2f}"
                )
            else:
                st.info("Le détail du score n'est pas disponible pour ce livre.")

            st.markdown("**Segments qui matchent**")
            if matches:
                for match in matches:
                    st.markdown(
                        f"- {match.get('segment', 'Segment')} : "
                        f"{match.get('text', '')} "
                        f"(score {match.get('score', 0.0):.2f})"
                    )
            else:
                st.caption("Aucun segment exploitable pour expliquer le matching.")

            st.markdown("**Pourquoi ce livre ?**")
            recap = (
                f"Score final {book.score:.2f}. "
                "Ce livre ressort car il s'aligne sur vos préférences principales "
                "et présente les meilleurs signaux sémantiques."
            )
            st.write(recap)

reco_df = _build_reco_dataframe(filtered_recos)
st.download_button(
    label="⬇️ Télécharger les recommandations (CSV)",
    data=reco_df.to_csv(index=False),
    file_name="recommandations_bookscout.csv",
    mime="text/csv",
    help="Export des recommandations filtrées : titre, auteur, genre, période, année, score.",
)
st.caption("Le fichier CSV contient les recommandations filtrées et leurs métadonnées principales.")

# LISTE BRUTE
with st.expander("📚 Voir les données brutes"):
    show_books(filtered_recos)

# ---------------------------------------------------------
# E. ACCESSIBILITE
# ---------------------------------------------------------
with st.expander("Accessibilité"):
    st.markdown(
        """
- Contraste suffisant et informations non transmises uniquement par la couleur.
- Taille de police lisible (compatible avec les réglages existants).
- Labels explicites pour chaque widget de filtre.
- Texte d'accompagnement pour interpréter les graphiques.
- Téléchargement CSV avec libellé clair et description du contenu.
"""
    )

st.markdown("<br><br>", unsafe_allow_html=True)
c_fin_1, c_fin_2, c_fin_3 = st.columns([1, 1, 1])
with c_fin_2:
    if st.button("🔄 Nouvelle Recherche", use_container_width=True):
        st.switch_page("pages/1_Questionnaire.py")
