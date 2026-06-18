def generate_recommendations(
    risk,
    risk_drivers
):

    recommendations = []

    if risk["chargeoff_rate"] > 10:

        recommendations.append(
            f"Portfolio charge-off rate is "
            f"{risk['chargeoff_rate']}%. "
            f"Review underwriting and approval criteria."
        )

    if (
        risk_drivers["top_grade"]["default_rate"]
        > 25
    ):

        recommendations.append(
            f"Grade "
            f"{risk_drivers['top_grade']['grade']} "
            f"exhibits a "
            f"{risk_drivers['top_grade']['default_rate']}% "
            f"default rate across "
            f"{risk_drivers['top_grade']['loan_count']} "
            f"loans. Review underwriting criteria."
        )

    if (
        risk_drivers["top_purpose"]["default_rate"]
        > 15
    ):

        recommendations.append(
            f"{risk_drivers['top_purpose']['purpose']} "
            f"loans exhibit a "
            f"{risk_drivers['top_purpose']['default_rate']}% "
            f"default rate across "
            f"{risk_drivers['top_purpose']['loan_count']} "
            f"loans. Review segment-specific performance."
        )

    if (
        risk_drivers["top_state"]["default_rate"]
        > 15
    ):

        recommendations.append(
            f"{risk_drivers['top_state']['state']} "
            f"exhibits a "
            f"{risk_drivers['top_state']['default_rate']}% "
            f"default rate across "
            f"{risk_drivers['top_state']['loan_count']} "
            f"loans. Monitor regional credit performance."
        )

    return recommendations