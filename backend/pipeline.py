from backend.profiler import profile_dataset
from backend.analytics.portfolio import portfolio_summary
from backend.analytics.risk import risk_summary
from backend.insights import generate_insight


def run_analysis(df):

    profile = profile_dataset(df)

    portfolio = portfolio_summary(df)

    risk = risk_summary(df)

    insight = generate_insight(
        portfolio,
        risk
    )

    return {
        "profile": profile,
        "portfolio": portfolio,
        "risk": risk,
        "insight": insight
    }