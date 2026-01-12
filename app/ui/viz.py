import math

import pandas as pd
import plotly.express as px
import streamlit as st


def show_coverage(coverage, embed_mode):
    st.markdown(f"Score de couverture global: **{coverage:.1f}%** (mode: {embed_mode})")


def show_books(book_recos):
    book_df = pd.DataFrame([book.__dict__ for book in book_recos])
    if book_df.empty:
        st.info("Aucun livre suggere.")
        return
    book_df["Score_pct"] = book_df["score"] * 100.0
    book_df["publication_year"] = book_df["publication_year"].fillna(
        book_df.get("publication_year_raw", "n/a")
    )
    book_df = book_df.fillna("n/a")
    book_df = book_df[
        (book_df["author"] != "n/a") & (book_df["author"].astype(str).str.len() > 0)
    ]
    book_df = book_df[
        (book_df["genres"] != "n/a") & (book_df["genres"].astype(str).str.len() > 0)
    ]
    book_df.rename(columns={"title": "Livre"}, inplace=True)
    st.dataframe(
        book_df[["Livre", "author", "genres", "publication_year", "Score_pct"]],
        use_container_width=True,
    )

    bar = px.bar(
        book_df.head(10),
        x="Livre",
        y="Score_pct",
        text="Score_pct",
        labels={"Score_pct": "Score (%)"},
    )
    bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    bar.update_layout(
        yaxis_range=[0, min(100, math.ceil(book_df["Score_pct"].max() + 10))]
    )
    st.plotly_chart(bar, use_container_width=True)

    genres = []
    for raw in book_df["genres"].dropna().astype(str):
        parts = [item.strip() for item in raw.replace("|", ";").split(";")]
        parts = [item for part in parts for item in part.split(",")]
        genres.extend([item.strip() for item in parts if item.strip()])
    if genres:
        genre_df = (
            pd.Series(genres)
            .value_counts()
            .head(10)
            .reset_index()
            .rename(columns={"index": "Genre", "count": "Count"})
        )
        genre_bar = px.bar(genre_df, x="Genre", y="Count", title="Genres dominants")
        st.plotly_chart(genre_bar, use_container_width=True)

    if "publication_year" in book_df.columns:
        year_series = pd.to_numeric(book_df["publication_year"], errors="coerce").dropna()
        if not year_series.empty:
            year_hist = px.histogram(
                year_series,
                nbins=20,
                title="Repartition des annees de publication",
            )
            st.plotly_chart(year_hist, use_container_width=True)

    for _, row in book_df.head(5).iterrows():
        st.markdown(
            f"**{row['Livre']}** ({row['author']}) - {row['summary']}"
        )


def show_similarity(similarities, answer_labels, book_titles):
    if similarities is None or similarities.size == 0:
        return
    heatmap = px.imshow(
        similarities,
        x=book_titles,
        y=answer_labels,
        color_continuous_scale="Blues",
    )
    heatmap.update_layout(height=400)
    st.plotly_chart(heatmap, use_container_width=True)


def show_synthesis(text, cached=False):
    if not text:
        return
    suffix = " (cache)" if cached else ""
    st.markdown(f"Synthese GenAI{suffix}:\n\n{text}")
