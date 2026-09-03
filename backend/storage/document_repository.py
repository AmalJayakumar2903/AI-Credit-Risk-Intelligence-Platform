from datetime import datetime

from backend.storage.mongopy import documents_collection


def save_document(
    filename,
    file_type,
    text,
    pages=None
):
    document = {
        "filename": filename,
        "file_type": file_type,
        "text": text,
        "pages": pages,
        "characters": len(text),
        "status": "ingested",
        "created_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(document)

    return str(result.inserted_id)