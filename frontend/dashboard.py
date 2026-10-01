import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="📊",
    layout="wide"
)


st.title("Credit Risk Analytics Platform")

st.caption(
    "Upload a financial dataset to analyze portfolio risk "
    "and interact with an AI risk analyst."
)


# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------

st.subheader("Dataset Analysis")

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)


if uploaded_file:

    st.caption(
        f"Selected: {uploaded_file.name}"
    )

    if st.button(
        "Analyze Dataset",
        type="primary"
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        with st.spinner(
            "Analyzing portfolio..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                # Store latest analysis
                st.session_state["analysis"] = result

                st.success(
                    "Analysis completed successfully."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure FastAPI is running on port 8000."
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"API request failed: {error}"
                )


# ---------------------------------------------------------
# Display analysis
# ---------------------------------------------------------

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    st.divider()

    st.header("Portfolio Overview")

    portfolio = result["portfolio"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Loans",
            f"{portfolio.get('total_loans', 0):,}"
        )

    with col2:
        st.metric(
            "Total Exposure",
            f"${portfolio.get('total_exposure', 0):,.0f}"
        )

    with col3:
        st.metric(
            "Average Loan",
            f"${portfolio.get('average_loan_amount', 0):,.0f}"
        )

    with col4:
        st.metric(
            "Average Interest Rate",
            f"{portfolio.get('average_interest_rate', 0):.2f}%"
        )


    # -----------------------------------------------------
    # Risk
    # -----------------------------------------------------

    st.header("Risk Metrics")

    risk = result["risk"]

    risk_cols = st.columns(
        len(risk)
    )

    for column, (key, value) in zip(
        risk_cols,
        risk.items()
    ):

        label = key.replace(
            "_",
            " "
        ).title()

        with column:

            if isinstance(value, float):

                st.metric(
                    label,
                    f"{value:.2f}%"
                )

            else:

                st.metric(
                    label,
                    str(value)
                )


    # -----------------------------------------------------
    # Segmentation
    # -----------------------------------------------------

    st.header("Risk Segmentation")

    segmentation = result.get(
        "segmentation",
        {}
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Grade",
            "Purpose",
            "State",
            "Credit Score"
        ]
    )


    with tab1:

        grade_data = segmentation.get(
            "grade_default_rate",
            {}
        )

        if grade_data:

            st.dataframe(
                grade_data,
                use_container_width=True
            )

        else:

            st.info(
                "No grade-level risk data available."
            )


    with tab2:

        purpose_data = segmentation.get(
            "purpose_default_rate",
            {}
        )

        if purpose_data:

            st.dataframe(
                purpose_data,
                use_container_width=True
            )

        else:

            st.info(
                "No purpose-level risk data available."
            )


    with tab3:

        state_data = segmentation.get(
            "state_default_rate",
            {}
        )

        if state_data:

            st.dataframe(
                state_data,
                use_container_width=True
            )

        else:

            st.info(
                "No state-level risk data available."
            )


    with tab4:

        fico_data = segmentation.get(
            "fico_default_rate",
            {}
        )

        if fico_data:

            st.dataframe(
                fico_data,
                use_container_width=True
            )

        else:

            st.info(
                "No credit-score risk data available."
            )


    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    st.header("Risk Recommendations")

    recommendations = result.get(
        "recommendations",
        []
    )

    if isinstance(
        recommendations,
        list
    ):

        for recommendation in recommendations:

            st.info(
                recommendation
            )

    else:

        st.write(
            recommendations
        )


    # -----------------------------------------------------
    # Insight
    # -----------------------------------------------------

    st.header("Portfolio Insight")

    insight = result.get(
        "insight"
    )

    if insight:

        st.write(
            insight
        )


    # -----------------------------------------------------
    # AI Analyst
    # -----------------------------------------------------

    st.divider()

    st.header("🤖 AI Risk Analyst")

    st.caption(
        "Ask questions about the latest portfolio analysis."
    )

    user_query = st.chat_input(
        "Ask something about this portfolio..."
    )

    if user_query:

        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing..."
            ):

                try:

                    ai_response = requests.post(
                        f"{API_URL}/ai/ask",
                        json={
                            "query": user_query,
                            "analysis_context": result
                        },
                        timeout=120
                    )

                    ai_response.raise_for_status()

                    answer = ai_response.json()

                    st.write(
                        answer["answer"]
                    )

                except requests.exceptions.RequestException as error:

                    st.error(
                        f"AI request failed: {error}"
                    )