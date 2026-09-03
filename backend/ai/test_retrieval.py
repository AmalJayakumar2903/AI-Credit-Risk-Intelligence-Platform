from backend.ai.document_retriever import search_documents


query = "What is the revised credit risk framework?"

documents = search_documents(
    query,
    n_results=3
)

print("Retrieved chunks:", len(documents))

for index, document in enumerate(documents, start=1):

    print()
    print(f"--- Chunk {index} ---")
    print(document)