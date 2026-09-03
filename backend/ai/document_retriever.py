from backend.storage.chroma import documents_collection


def search_documents(
    query,
    n_results=3
):

    results = documents_collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents