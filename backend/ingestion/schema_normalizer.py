def normalize_schema(df, schema_mapping):

    rename_map = {

        actual_column:
        canonical_column

        for canonical_column,
        actual_column

        in schema_mapping.items()

    }

    df = df.rename(
        columns=rename_map
    )

    return df