import pandas as pd

def grade_distribution(df):
    return (
        df["grade"]
        .value_counts()
        .to_dict()
    )

def purpose_distribution(df):
    return (
        df["purpose"]
        .value_counts()
        .to_dict()
    )

def state_distribution(df):
    return (
        df["addr_state"]
        .value_counts()
        .head(10)
        .to_dict()
    )

def grade_default_rate(df):
    defaults = (
        df.assign(
            default_flag=
            (df["loan_status"] == "Charged Off")
        )
        .groupby("grade")["default_flag"]
        .mean()
        * 100
    )
    return defaults.round(2).to_dict()

def purpose_default_rate(df):
    defaults = (
        df.assign(
            default_flag=
            (df["loan_status"] == "Charged Off")
        )
        .groupby("purpose")["default_flag"]
        .mean()
        * 100
    )
    return defaults.round(2).to_dict()

def fico_default_rate(df):
    fico_band = pd.cut(
        df["fico_range_low"],
        bins=[300, 580, 670, 740, 800, 900],
        labels=[
            "Poor",
            "Fair",
            "Good",
            "Very Good",
            "Excellent"
        ]
    )

    defaults = (
        df.assign(
            fico_band=fico_band,
            default_flag=
            (df["loan_status"] == "Charged Off")
        )
        .groupby("fico_band")["default_flag"]
        .mean()
        * 100
    )
    return defaults.round(2).to_dict()

def state_default_rate(df):

    state_defaults = (
        df.assign(
            default_flag=
            (df["loan_status"] == "Charged Off")
        )
        .groupby("addr_state")
        ["default_flag"]
        .mean()
        * 100
    )

    return (
        state_defaults
        .round(2)
        .to_dict()
    )