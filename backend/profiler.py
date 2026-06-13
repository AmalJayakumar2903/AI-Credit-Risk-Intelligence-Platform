import pandas as pd

def profile_dataset(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": (
            df.isnull()
              .sum()
              .sort_values(ascending=False)
              .head(10)
              .to_dict()
        )
    }