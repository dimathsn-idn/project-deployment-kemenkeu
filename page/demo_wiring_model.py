from ui.widgets import banner
import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


@st.cache_resource
def load_assets():
    import time
    time.sleep(2)

    with open("assets/model/iris/classifier.pkl", "rb") as f:
        classifier = pickle.load(f)
    with open("assets/model/iris/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    
    return classifier, label_encoder


def render() -> None:
    banner(
        "Wiring Model",
        "Mengenal konsep wiring model untuk menghubungkan berbagai komponen dalam aplikasi Streamlit.",
    )

    classifier, label_encoder = load_assets()
    st.write("Model berhasil di-load menggunakan wiring model!")

    with st.form("Iris classification form"):
        sepal_length = st.number_input("Sepal Length", min_value=0.0, step=0.1)
        sepal_width = st.number_input("Sepal Width", min_value=0.0, step=0.1)
        petal_length = st.number_input("Petal Length", min_value=0.0, step=0.1)
        petal_width = st.number_input("Petal Width", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Predict")
    
    if submitted:
        input_df = pd.DataFrame(
            [[sepal_length, sepal_width, petal_length, petal_width]],
            columns=["sepal_length", "sepal_width", "petal_length", "petal_width"]
        )

        st.write("Input Data:")
        st.dataframe(input_df)

        prediction = classifier.predict(input_df)[0]

        st.write(f"Predicted Class: `{prediction}`")
        st.write(f"Predicted Species: `{label_encoder.inverse_transform([prediction])[0]}`")
