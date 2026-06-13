def generate_insight(portfolio, risk):

    return f"""
Portfolio contains {portfolio['total_loans']} loans.

Total exposure is ${portfolio['total_exposure']:,.0f}.

Average loan size is ${portfolio['average_loan_amount']:,.0f}.

Average interest rate is {portfolio['average_interest_rate']:.2f}%.

Charge-off rate is {risk['chargeoff_rate']}%.

Fully paid rate is {risk['fully_paid_rate']}%.

Current loan rate is {risk['current_rate']}%.
"""