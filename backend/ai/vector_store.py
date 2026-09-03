import chromadb


client = chromadb.PersistentClient(
    path="data/chroma"
)


collection = client.get_or_create_collection(
    name="credit_risk_analysis"
)


def store_analysis_context(
    analysis_id,
    portfolio,
    risk,
    risk_drivers,
    recommendations
):

    document = f"""
    Portfolio:
    {portfolio}

    Risk:
    {risk}

    Risk Drivers:
    {risk_drivers}

    Recommendations:
    {recommendations}
    """

    collection.upsert(

        ids=[
            f"analysis_{analysis_id}"
        ],

        documents=[
            document
        ],

        metadatas=[
            {
                "analysis_id":
                    str(analysis_id)
            }
        ]

    )


def search_analysis_context(
    query,
    n_results=3
):

    results = collection.query(

        query_texts=[
            query
        ],

        n_results=n_results

    )

    return results