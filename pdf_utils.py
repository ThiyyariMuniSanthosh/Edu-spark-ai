"""PDF checks and text extraction (PyMuPDF)."""
import fitz  # PyMuPDF

MAX_UPLOAD_MB = 10
MAX_PAGES = 200


class PDFError(Exception):
    """A problem with the uploaded file, shown to the user as-is."""


def extract_pdf_text(file_bytes, filename):
    if not filename.lower().endswith(".pdf"):
        raise PDFError("Only PDF files are supported in this version.")
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        raise PDFError(f"This file is {size_mb:.1f} MB. The limit is {MAX_UPLOAD_MB} MB.")
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFError("This file could not be opened as a PDF.") from exc
    try:
        if doc.needs_pass:
            raise PDFError("This PDF is password-protected. Upload an unlocked copy.")
        if doc.page_count > MAX_PAGES:
            raise PDFError(f"This PDF has {doc.page_count} pages. The limit is {MAX_PAGES}.")
        pages = [page.get_text().strip() for page in doc]
    finally:
        doc.close()
    text = "\n\n".join(p for p in pages if p)
    if not text:
        raise PDFError("No readable text found. Scanned PDFs need OCR, which this version does not do.")
    return text
