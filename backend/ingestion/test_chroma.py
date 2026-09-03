from bson import ObjectId

from backend.storage.mongopy import documents_collection
from backend.ingestion.chroma_ingestion import ingest_document


document = documents_collection.find_one(
    {"filename": "BaselDoc.pdf"}
)

if not document:
    raise ValueError(
        "BaselDoc.pdf not found in MongoDB"
    )

result = ingest_document(
    document["_id"]
)

print("Document:", result["document_id"])
print("Chunks:", result["chunks"])
print("Status: stored in ChromaDB")