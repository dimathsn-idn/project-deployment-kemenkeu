from ui.widgets import banner
import streamlit as st
from utils.ollama_client import list_models, stream_text

def render() -> None:
    banner(
        "Integrasi Endpoint Model / LLM",
        "Menghubungkan model machine learning atau LLM ke aplikasi Streamlit, menyiapkan endpoint API, dan langkah-langkah untuk deployment ke platform cloud.",
    )

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    selected_model = st.selectbox("Pilih model Ollama:", options=list_models(), key="ollama_model")

    st.divider()

    # Tampilkan history chat
    for msg in st.session_state['messages']:
        with st.chat_message(msg['role']):
            st.write(msg['content'])

    # Input
    prompt = st.chat_input("Masukkan prompt...")

    if prompt:
        if not selected_model:
            st.warning("Pilih model Ollama terlebih dahulu.")
            return

        # Tampilkan pesan user langsung
        with st.chat_message("user"):
            st.write(prompt)

        # Append user message ke history
        st.session_state['messages'].append({
            "role": "user",
            "content": prompt
        })

        # Stream response assistant
        with st.chat_message("assistant"):
            try:
                response_text = st.write_stream(
                    stream_text(st.session_state['messages'], selected_model)
                )
                st.session_state['messages'].append({
                    "role": "assistant",
                    "content": response_text
                })
            except Exception as exc:
                st.error(f"Gagal generate text: {exc}")
