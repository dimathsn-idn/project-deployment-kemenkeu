from ui.widgets import banner
import streamlit as st
import pandas as pd


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

    _init_state()

    # tanpa state
    counter = 0
    if st.button("Increment Counter Tanpa State"):
        counter += 1
    st.write(f"Counter Tanpa State: {counter}")

    st.divider()

    # dengan state
    if st.button("Increment Counter Dengan State"):
        st.session_state['state_demo_counter'] += 1

    st.write( f"State Counter: {st.session_state.state_demo_counter}")

    # cache
    @st.cache_data
    def _get_dataset() -> pd.DataFrame:
        import time

        time.sleep(2)  # Simulate expensive computation
        return _get_cached_dataset(size=1000, seed=st.session_state.state_demo_seed)
    
    st.write("Dataset:")
    import datetime
    start = datetime.datetime.now()
    st.dataframe(_get_dataset())
    end = datetime.datetime.now()
    st.write(f"Data loaded in {(end - start).total_seconds():.2f} seconds")

    # Load expensive model
    @st.cache_resource(ttl=10)
    def _load_expensive_model():
        import time

        time.sleep(3)  # Simulate expensive model loading
        return "Model LLM Siap!"
    
    if st.button("Load Expensive Model"):
        with st.spinner("Loading model..."):
            model = _load_expensive_model()
        st.success(model)
