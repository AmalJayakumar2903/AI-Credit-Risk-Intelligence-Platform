from backend.ai.risk_explainer import (
    generate_risk_explanation
)


portfolio = {
    "total_loans": 2000,
    "total_exposure": 30664050.0,
    "average_loan_amount": 15332.03,
    "average_interest_rate": 12.24
}


risk = {
    "chargeoff_rate": 14.7,
    "fully_paid_rate": 73.7,
    "current_rate": 11.05
}


risk_drivers = {
    "top_grade": {
        "grade": "E",
        "default_rate": 28.87,
        "loan_count": 142
    }
}


recommendations = [
    "Review exposure to higher-risk credit grades.",
    "Monitor portfolio segments with elevated default rates."
]


response = generate_risk_explanation(
    portfolio,
    risk,
    risk_drivers,
    recommendations
)


print(response)