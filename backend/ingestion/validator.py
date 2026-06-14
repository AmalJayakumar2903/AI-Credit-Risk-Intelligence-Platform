REQUIRED_CREDIT_COLUMNS = [
    "loan_amnt",
    "loan_status"
]


RECOMMENDED_COLUMNS = [
    "int_rate",
    "annual_inc",
    "grade",
    "fico_range_low"
]


def validate_credit_dataset(df):

    columns = set(df.columns)

    required_present = [
        col for col in REQUIRED_CREDIT_COLUMNS
        if col in columns
    ]

    recommended_present = [
        col for col in RECOMMENDED_COLUMNS
        if col in columns
    ]

    confidence = (
        len(required_present) * 40 +
        len(recommended_present) * 5
    )

    confidence = min(confidence, 100)

    return {
        "is_credit_dataset":
            len(required_present)
            == len(REQUIRED_CREDIT_COLUMNS),

        "confidence_score":
            confidence,

        "required_found":
            required_present,

        "recommended_found":
            recommended_present
    }