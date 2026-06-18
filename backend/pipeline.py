from backend.profiler import profile_dataset
from backend.analytics.portfolio import portfolio_summary
from backend.analytics.risk import risk_summary
from backend.insights import generate_insight
from backend.ingestion.data_dictionary import generate_data_dictionary
from backend.ingestion.validator import validate_credit_dataset
from backend.ingestion.cleaner import clean_dataset
from backend.analytics.segmentation import (
    grade_distribution,
    purpose_distribution,
    state_distribution,
    state_default_rate,
    grade_default_rate,
    purpose_default_rate,
    fico_default_rate
)
from backend.analytics.risk_drivers import (
    top_risk_grade,
    top_risk_purpose,
    top_risk_state
)
from backend.analytics.recommendations import (
    generate_recommendations
)

def run_analysis(df):

    df, cleaning_report = clean_dataset(df)
    profile = profile_dataset(df)
    data_dictionary = generate_data_dictionary(df)
    validation = validate_credit_dataset(df)

    portfolio = portfolio_summary(df)

    risk = risk_summary(df)
    segmentation = {

        "grade_distribution":
            grade_distribution(df),

        "purpose_distribution":
            purpose_distribution(df),

        "state_distribution":
            state_distribution(df),

        "state_default_rate":
            state_default_rate(df),

        "grade_default_rate":
            grade_default_rate(df),

        "purpose_default_rate":
            purpose_default_rate(df),

        "fico_default_rate":
            fico_default_rate(df)

    }

    risk_drivers = {

        "top_grade":
            top_risk_grade(
                segmentation
            ),

        "top_purpose":
            top_risk_purpose(
                segmentation
            ),

        "top_state":
            top_risk_state(
                segmentation
            )
    }

    recommendations = generate_recommendations(
        risk,
        risk_drivers
    )
    

    insight = generate_insight(
        portfolio,
        risk,
        segmentation,
        risk_drivers
    )

    return {
        "profile": profile,
        "data_dictionary": data_dictionary,
        "portfolio": portfolio,
        "risk": risk,
        "segmentation": segmentation,
        "insight": insight,
        "validation": validation,
        "cleaning_report": cleaning_report,
        "risk_drivers": risk_drivers,
        "recommendations": recommendations
    }