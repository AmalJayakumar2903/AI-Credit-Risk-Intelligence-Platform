import pandas as pd

DROP_COLUMNS = [
    "member_id",
    "url"
]

CATEGORICAL_FILL = [
    "emp_title",
    "title"
]

MEDIAN_FILL = [
    "mths_since_rcnt_il",
    "mo_sin_old_il_acct",
    "bc_open_to_buy",
    "bc_util",
    "percent_bc_gt_75",
    "mths_since_recent_inq",
    "il_util",
    "num_tl_120dpd_2m"
]


def clean_dataset(df):

    report = {
        "rows_before": len(df),
        "columns_before": len(df.columns)
    }

    df = df.copy()

    # Remove duplicates
    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # Drop unnecessary columns
    existing_drop_cols = [
        col for col in DROP_COLUMNS
        if col in df.columns
    ]

    df = df.drop(
        columns=existing_drop_cols,
        errors="ignore"
    )

    # Fill categoricals
    for col in CATEGORICAL_FILL:

        if col in df.columns:

            df[col] = df[col].fillna(
                "UNKNOWN"
            )

    # Fill numerics
    for col in MEDIAN_FILL:

        if col in df.columns:

            df[col] = df[col].fillna(
                df[col].median()
            )

    report["duplicates_removed"] = duplicates_removed
    report["columns_dropped"] = existing_drop_cols
    report["rows_after"] = len(df)
    report["columns_after"] = len(df.columns)

    return df, report