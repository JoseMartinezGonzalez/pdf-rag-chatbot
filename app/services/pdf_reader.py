from pypdf import PdfReader
import re
from app.utils.text_cleaner import clean_text

def extract_text_from_pdf(pdf_bytes: bytes, chunk_size: int = 800, overlap: int = 100):
    reader = PdfReader(pdf_bytes)
    text = []
    for page in reader.pages:
        try:
            text.append(page.extract_text() or "")
        except Exception:
            continue
    full = "\n".join(text)
    full = clean_text(full)
    # chunking
    chunks = []
    i = 0
    while i < len(full):
        chunk = full[i:i+chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    # filter short chunks
    chunks = [c.strip() for c in chunks if len(c.strip()) > 50]
    return chunks
