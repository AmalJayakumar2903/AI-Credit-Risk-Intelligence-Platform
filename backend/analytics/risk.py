def risk_summary(df):

    total = len(df)

    charged_off = (
        (df["loan_status"] == "Charged Off")
        .sum()
    )

    fully_paid = (
        (df["loan_status"] == "Fully Paid")
        .sum()
    )

    current = (
        (df["loan_status"] == "Current")
        .sum()
    )

    return {
        "chargeoff_rate":
            float(round(charged_off / total * 100, 2)),

        "fully_paid_rate":
            float(round(fully_paid / total * 100, 2)),

        "current_rate":
            float(round(current / total * 100, 2))
    }