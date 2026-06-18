def generate_recommendations(
    risk,
    risk_drivers
):

    recommendations = []

    if risk["chargeoff_rate"] > 10:

        recommendations.append(
            "Portfolio charge-off rate exceeds 10%. Review underwriting and approval criteria."
        )

    if (
        risk_drivers["top_grade"]["default_rate"]
        > 25
    ):

        recommendations.append(
            f"Review Grade {risk_drivers['top_grade']['grade']} lending strategy due to elevated default rates."
        )

    if (
        risk_drivers["top_purpose"]["default_rate"]
        > 15
    ):

        recommendations.append(
            f"Investigate {risk_drivers['top_purpose']['purpose']} loans due to elevated portfolio losses."
        )

    if (
        risk_drivers["top_state"]["default_rate"]
        > 15
    ):

        recommendations.append(
            f"Monitor credit performance in {risk_drivers['top_state']['state']}."
        )

    return recommendations