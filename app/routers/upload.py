from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_reader import extract_text_from_pdf
from app.services.embeddings import EmbeddingsManager

router = APIRouter()

EMB_STORE = EmbeddingsManager()  # loads existing index if present

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")
    # read bytes
    content = await file.read()
    text_chunks = extract_text_from_pdf(content)
    # add to embeddings & persist
    EMB_STORE.add_documents(text_chunks, source=file.filename)
    return {"status": "ok", "chunks_added": len(text_chunks)}
