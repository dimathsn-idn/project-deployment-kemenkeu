import streamlit as st

KEMENKEU_BLUE = "#0F2D6B"
KEMENKEU_GOLD = "#F2B705"
KEMENKEU_BG = "#F6F8FC"


def setup_page() -> None:
    st.set_page_config(
        page_title="Project Kemenkeu",
        page_icon="🧠",
        layout="wide",
    )


def apply_kemenkeu_theme() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {KEMENKEU_BG};
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        .kemenkeu-banner {{
            background: linear-gradient(90deg, {KEMENKEU_BLUE} 0%, #1F4AA8 100%);
            padding: 1rem 1.2rem;
            border-radius: 12px;
            color: white;
            border-bottom: 2px solid {KEMENKEU_GOLD};
            margin-top: 1rem;
            margin-bottom: 1rem;
        }}
        .kemenkeu-card {{
            background: #ffffff;
            border: 1px solid color-mix(in srgb, {KEMENKEU_BLUE} 20%, #dfe5f2);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 14px rgba(15, 45, 107, 0.08);
        }}
        .kemenkeu-card h4 {{
            margin-top: 0;
            margin-bottom: 0.45rem;
            color: {KEMENKEU_BLUE};
        }}
        .kemenkeu-card p {{
            margin-top: 0;
            margin-bottom: 0.75rem;
            color: #2a3550;
        }}
        .kemenkeu-link-btn {{
            display: inline-block;
            margin-top: 0.25rem;
            padding: 0.45rem 0.8rem;
            border-radius: 10px;
            border: 1px solid {KEMENKEU_GOLD};
            background: color-mix(in srgb, {KEMENKEU_GOLD} 14%, white);
            color: #7d5a00;
            text-decoration: none;
            font-weight: 500;
        }}
        .kemenkeu-link-btn:hover {{
            background: {KEMENKEU_GOLD};
            color: #1f2430;
        }}
        h1, h2, h3 {{
            color: {KEMENKEU_BLUE};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
