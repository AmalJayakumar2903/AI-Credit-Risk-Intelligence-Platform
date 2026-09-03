from backend.ingestion.pdf_loader import extract_ocr_text
from backend.storage.document_repository import save_document


pdf_path = "data/raw/BaselDoc.pdf"

text = extract_ocr_text(pdf_path)

document_id = save_document(
    filename="BaselDoc.pdf",
    file_type="pdf",
    text=text,
    pages=2
)

print("Document ID:", document_id)
print("Characters:", len(text))
print("Status: ingested")