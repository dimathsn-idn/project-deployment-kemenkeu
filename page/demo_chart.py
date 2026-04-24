import streamlit as st
from ui.widgets import banner
import pandas as pd
from numpy.random import default_rng as rng
import plotly.figure_factory as ff


def render() -> None:
    banner(
        "Demo Chart",
        "Contoh penggunaan chart dengan Streamlit",
    )

    with st.expander("Lihat Contoh Chart"):
        hist_data = [
            rng(0).standard_normal(200) - 2,
            rng(1).standard_normal(200),
            rng(2).standard_normal(200) + 2,
        ]
        group_labels = ["Group 1", "Group 2", "Group 3"]

        fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[0.1, 0.25, 0.5]
        )

        st.plotly_chart(fig)

    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        st.metric("Contoh Metric 1", value="75%", delta="+5%", border=True)
    with metric2:
        st.metric("Contoh Metric 2", value="50%", delta="-3%", border=True)
    with metric3:
        st.metric("Contoh Metric 3", value="90%", delta="+10%", border=True)
    with metric4:
        st.metric("Contoh Metric 4", value="60%", delta="-2%", border=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Line Chart")
        st.line_chart([[1,2,],[5,4,],[3,6],[4,7],[5,8],[6,9],[7,10],[8,11],[9,12],[10,13]])
    with col2:
        st.subheader("Bar Chart")
        st.bar_chart([1,5,3,6,2,7,4,8,5,9])
    with col3:
        st.subheader("Scatter Chart")
        st.scatter_chart([[1,2,],[5,4,],[3,6],[4,7],[5,8],[6,9],[7,10],[8,11],[9,12],[10,13]])
    
    st.divider()

    st.write("# Contoh penggunaan dataframe untuk chart:")
    dataset = {
        "normal": "data/normal.csv",
        "promosi": "data/promosi.csv",
        "musiman": "data/musiman.csv",
    }

    options = ["normal", "promosi", "musiman"]
    choosen_set = st.selectbox(
        "Pilih dataset",
        # options=list(dataset.keys()),
        options=options,
    )

    st.write(f"Dataset yang dipilih: `{choosen_set}`")
    st.write(f"URL dataset: `{dataset[choosen_set]}`")

    with st.expander("Lihat Dataframe"):
        df = pd.read_csv(dataset[choosen_set])
        st.write(df)

    st.plotly_chart(
        {
            "data": [
                {
                    "x": df.hari.tolist(),
                    "y": df.penjualan.tolist(),
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Penjualan"
                },
                {
                    "x": df.hari.tolist(),
                    "y": df.baseline.tolist(),
                    "type": "scatter",
                    "mode": "lines",
                    "name": "Baseline",
                    "line": {"dash": "dash", "color": "red"}
                }
            ],
            "layout": {
                "title": f"Penjualan Harian - Dataset `{choosen_set}`",
                "xaxis": {"title": "Hari"},
                "yaxis": {"title": "Penjualan"},
                "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
            }
        }
    )