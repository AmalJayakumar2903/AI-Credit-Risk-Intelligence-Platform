def generate_data_dictionary(df):

    dictionary = {}

    total_rows = len(df)

    for column in df.columns:

        dictionary[column] = {
            "dtype": str(df[column].dtype),
            "missing_count": int(df[column].isnull().sum()),
            "missing_pct": round(
                (df[column].isnull().sum() / total_rows) * 100,
                2
            ),
            "unique_count": int(
                df[column].nunique(dropna=True)
            )
        }

    return dictionary