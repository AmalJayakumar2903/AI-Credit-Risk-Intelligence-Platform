from backend.ingestion.schema_mapper import map_schema
from backend.ingestion.dataset_types import DATASET_TYPES


def classify_dataset(df):

    mappings = map_schema(df)

    scores = {}

    for dataset_type, schema in DATASET_TYPES.items():

        required = schema["required"]

        recommended = schema.get(
            "recommended",
            []
        )

        required_found = [

            col
            for col in required
            if col in mappings
        ]

        recommended_found = [

            col
            for col in recommended
            if col in mappings
        ]

        score = (
            (
                len(required_found)
                * 3
            )
            +
            len(recommended_found)
        )

        scores[dataset_type] = {

            "score":
                score,

            "required_found":
                required_found,

            "recommended_found":
                recommended_found
        }

    best_type = max(
        scores,
        key=lambda x:
        scores[x]["score"]
    )

    best_score = scores[
        best_type
    ]

    return {

        "dataset_type":
            best_type,

        "confidence":
            round(
                (
                    best_score["score"]
                    /
                    (
                        len(
                            DATASET_TYPES[
                                best_type
                            ]["required"]
                        ) * 3
                        +
                        len(
                            DATASET_TYPES[
                                best_type
                            ].get(
                                "recommended",
                                []
                            )
                        )
                    )
                ) * 100,
                2
            ),

        "schema_mapping":
            mappings,

        "required_found":
            best_score[
                "required_found"
            ],

        "recommended_found":
            best_score[
                "recommended_found"
            ]
    }