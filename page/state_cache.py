from ui.widgets import banner
import streamlit as st
import pandas as pd


@st.cache_data(ttl=20)
def _get_cached_dataset(size: int, seed: int) -> pd.DataFrame:
    """Simulate expensive data generation and cache the result for repeated runs."""
    base = pd.date_range("2026-01-01", periods=size, freq="D")
    revenue = [((idx * 37 + seed * 11) % 700) + 300 for idx in range(size)]
    cost = [int(val * 0.68) for val in revenue]
    region = ["Barat" if idx % 2 == 0 else "Timur" for idx in range(size)]

    return pd.DataFrame(
        {
            "tanggal": base,
            "wilayah": region,
            "revenue": revenue,
            "cost": cost,
            "profit": [rev - cst for rev, cst in zip(revenue, cost)],
        }
    )


def _init_state() -> None:
    st.session_state.setdefault("state_demo_counter", 0)
    st.session_state.setdefault("state_demo_region", "Semua")
    st.session_state.setdefault("state_demo_seed", 7)
    st.session_state.setdefault("state_demo_cache_cleared_at", "Belum pernah")


def render() -> None:
    banner(
        "State dan Cache",
        "Berkenalan dengan konsep state management dan caching untuk meningkatkan performa aplikasi Streamlit.",
    )
