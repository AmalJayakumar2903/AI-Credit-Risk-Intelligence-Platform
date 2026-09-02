import streamlit as st
import requests

st.title(
    "Credit Risk Analytics Platform"
)

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            uploaded_file.type
        )
    }

    if st.button("Analyze Dataset"):

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files=files
        )

        result = response.json()

        st.subheader(
            "Portfolio Metrics"
        )

        st.json(
            result["portfolio"]
        )

        st.subheader(
            "Risk Metrics"
        )

        st.json(
            result["risk"]
        )

        st.subheader(
            "Recommendations"
        )

        st.json(
            result["recommendations"]
        )

        st.subheader(
            "Insights"
        )

        st.write(
            result["insight"]
        )