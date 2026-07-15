import pandas as pd


def portfolio_summary(df):

    return {
        "total_loans": len(df),

        "total_exposure":
            float(df["loan_amount"].sum()),

        "average_loan_amount":
            float(df["loan_amount"].mean()),

        "average_interest_rate":
            float(
                df["interest_rate"]
                .astype(str)
                .str.replace("%", "", regex=False)
                .astype(float)
                .mean()
            )
    }