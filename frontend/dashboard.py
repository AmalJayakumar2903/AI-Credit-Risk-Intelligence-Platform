import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------------
# Page
# ---------------------------------------------------------

st.title("Credit Risk Analytics Platform")

st.caption(
    "Upload a financial dataset to analyze portfolio risk "
    "and interact with an AI risk analyst."
)


# ---------------------------------------------------------
# Dataset upload
# ---------------------------------------------------------

st.header("Dataset Analysis")

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

                # Persist analysis across Streamlit reruns
                st.session_state.analysis = result

                # Clear previous AI conversation
                st.session_state.chat_history = []

                st.success(
                    "Analysis completed successfully."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend."
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"API request failed: {error}"
                )


# ---------------------------------------------------------
# Display analysis
# ---------------------------------------------------------

if st.session_state.analysis:

    result = st.session_state.analysis

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
    # Risk metrics
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
        st.write(insight)


# ---------------------------------------------------------
# AI Risk Analyst
# ---------------------------------------------------------

st.divider()

st.header("🤖 AI Risk Analyst")

if not st.session_state.analysis:

    st.info(
        "Run a dataset analysis first to enable the AI Risk Analyst."
    )

else:

    st.caption(
        "Ask questions about the latest portfolio analysis."
    )

    # Display previous conversation
    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # Persistent chat input
    user_query = st.chat_input(
        "Ask about this portfolio..."
    )


    if user_query:

        # Store user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        with st.chat_message("user"):
            st.write(user_query)


        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/ai/ask",
                        json={
                            "query": user_query,
                            "analysis_context":
                                st.session_state.analysis
                        },
                        timeout=120
                    )

                    response.raise_for_status()

                    answer = response.json()["answer"]

                    st.write(answer)

                    # Store AI response
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except requests.exceptions.RequestException as error:

                    error_message = (
                        f"AI request failed: {error}"
                    )

                    st.error(
                        error_message
                    )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )