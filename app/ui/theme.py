import streamlit as st


def apply_book_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&family=Literata:wght@400;600;700&display=swap');

        :root {
            --paper: #eef6f1;
            --ink: #17211b;
            --muted: #3f5a4a;
            --accent: #f62d23;
            --accent-dark: #9dc7f2;
            --panel: rgba(255, 255, 255, 0.9);
            --border: #f62d23;
            --lichen: #f62d23;
        }

        html, body, [class*="css"] {
            font-family: "Space Grotesk", sans-serif;
            color: var(--ink);
        }

        .stApp {
            background: linear-gradient(160deg, #f2fbf6 0%, #e6f3ec 45%, #f8fbf9 100%);
        }

        [data-testid="stSidebar"] {
            background: var(--lichen);
            border-right: 1px solid #bcd3c1;
        }

        [data-testid="stSidebar"] * {
            color: #000000 !important;
        }

        [data-testid="stSidebarNav"]::before {
            content: "Recommandation litteraire";
            display: block;
            font-family: "Literata", serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #000000;
            padding: 0.6rem 0.25rem 0.75rem 0.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 0.5rem;
        }

        .sidebar-title {
            font-family: "Literata", serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #000000;
            padding: 0.5rem 0.25rem 0.75rem 0.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 0.5rem;
        }

        [data-testid="stHeader"] {
            background: var(--accent);
            border-bottom: 1px solid #b7c8a8;
        }

        [data-testid="stHeader"] * {
            color: #000000 !important;
        }

        h1, h2, h3, h4, .stTitle, .stHeader, .stSubheader,
        [data-testid="stHeader"] h1, [data-testid="stHeader"] h2,
        [data-testid="stHeader"] h3, [data-testid="stHeader"] h4,
        [data-testid="stHeading"] {
            font-family: "Literata", serif;
            letter-spacing: 0.3px;
            color: var(--ink) !important;
        }

        h1 {
            color: var(--accent-dark);
        }

        .stCaption {
            color: var(--muted);
        }

        .stMarkdown, .stMarkdown p, .stMarkdown span,
        .stTextInput label, .stTextArea label, .stSelectbox label,
        .stMultiSelect label, .stSlider label, label,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stForm"] label,
        .stCaption {
            color: var(--ink) !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #9aa3b2 !important;
        }

        .block-container {
            padding-top: 2rem;
        }

        .stForm {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 14px 40px rgba(31, 36, 48, 0.08);
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stMultiSelect div, .stSlider {
            background-color: #ffffff !important;
            color: var(--ink) !important;
            border: 1px solid var(--accent) !important;
            border-radius: 10px !important;
        }

        /* Streamlit/BaseWeb slider track (not a native input[type=range]) */
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
            background-color: var(--accent) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] div[aria-hidden="true"] {
            background: var(--accent) !important;
        }

        [data-testid="stSlider"] [role="slider"] {
            background: var(--accent) !important;
            border: 2px solid #e2efff !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--accent), #ff8f5a);
            color: #ffffff;
            border: none;
            border-radius: 999px;
            padding: 0.45rem 1.6rem;
            font-weight: 600;
            box-shadow: 0 10px 20px rgba(255, 107, 61, 0.25);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, var(--accent-dark), #ff6b3d);
            color: #ffffff;
        }

        .stDataFrame {
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
