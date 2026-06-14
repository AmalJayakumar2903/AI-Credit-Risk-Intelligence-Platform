from backend.profiler import profile_dataset
from backend.analytics.portfolio import portfolio_summary
from backend.analytics.risk import risk_summary
from backend.insights import generate_insight
from backend.ingestion.data_dictionary import generate_data_dictionary
from backend.ingestion.validator import validate_credit_dataset
from backend.ingestion.cleaner import clean_dataset

def run_analysis(df):

    df, cleaning_report = clean_dataset(df)
    profile = profile_dataset(df)
    data_dictionary = generate_data_dictionary(df)
    validation = validate_credit_dataset(df)

    portfolio = portfolio_summary(df)

    risk = risk_summary(df)

    insight = generate_insight(
        portfolio,
        risk
    )

    return {
        "profile": profile,
        "data_dictionary": data_dictionary,
        "portfolio": portfolio,
        "risk": risk,
        "insight": insight,
        "validation": validation,
        "cleaning_report": cleaning_report
    }