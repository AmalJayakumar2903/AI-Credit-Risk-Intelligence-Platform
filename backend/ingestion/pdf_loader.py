from pathlib import Path
from pypdf import PdfReader


def extract_text(file_path):
    reader = PdfReader(file_path)
    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_ocr_text(file_path):
    pdf_path = Path(file_path)

    text_files = sorted(
        pdf_path.parent.glob(
            f"{pdf_path.stem}_page-*.txt"
        )
    )

    if not text_files:
        raise FileNotFoundError(
            f"No OCR text files found for {pdf_path.name}"
        )

    pages = []

    for text_file in text_files:
        text = text_file.read_text(
            encoding="utf-8",
            errors="ignore"
        ).strip()

        if text:
            pages.append(text)

    return "\n\n".join(pages)