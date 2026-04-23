import streamlit as st


def banner(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="kemenkeu-banner">
            <h3 style="margin:0; color:white;">{title}</h3>
            <p style="margin:0.25rem 0 0 0; opacity:0.95;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_with_anchor(title: str, content: str, anchor: str, label: str = "Buka Selengkapnya") -> None:
    st.markdown(
        f"""
        <div class="kemenkeu-card">
            <h4>{title}</h4>
            <p>{content}</p>
            <a class="kemenkeu-link-btn" href="{anchor}">
                {label}
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
