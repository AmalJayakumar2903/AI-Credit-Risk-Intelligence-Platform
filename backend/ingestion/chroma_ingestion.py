from backend.storage.mongopy import documents_collection as mongo_documents
from backend.storage.chroma import documents_collection as chroma_documents


def ingest_document(document_id):

    document = mongo_documents.find_one(
        {"_id": document_id}
    )

    if not document:
        raise ValueError(
            "Document not found in MongoDB"
        )

    text = document["text"]

    chunk_size = 500
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    ids = []

    for index in range(len(chunks)):
        ids.append(
            f"{document_id}_chunk_{index}"
        )

    metadatas = [
        {
            "document_id": str(document_id),
            "filename": document["filename"],
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    chroma_documents.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return {
        "document_id": str(document_id),
        "chunks": len(chunks)
    }