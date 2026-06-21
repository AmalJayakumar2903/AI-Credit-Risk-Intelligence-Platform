from backend.ingestion.schema_aliases import COLUMN_ALIASES


def map_schema(df):

    mappings = {}

    columns = [
        col.lower()
        for col in df.columns
    ]

    for canonical_name, aliases in COLUMN_ALIASES.items():

        for alias in aliases:

            if alias.lower() in columns:

                mappings[canonical_name] = alias

                break

    return mappings