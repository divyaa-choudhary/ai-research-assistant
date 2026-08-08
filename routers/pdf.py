from fastapi import APIRouter, HTTPException
from utils.logger import get_logger
from schemas.pdf import LoadedDocOut, LoadAllOut
from loaders.pdf_loader import load_all_pdfs 

logger = get_logger(__name__)
router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.get("/load-all", response_model=LoadAllOut)
def load_all_documents():
    try:
        results = load_all_pdfs()
    except Exception:
        logger.exception("Failed to load PDFs")
        raise HTTPException(status_code=500, detail="Failed to load PDF documents")
    
    docs = [LoadedDocOut(file_name=doc["file_name"], char_count=len(doc["text"]), preview=doc["text"][-2000:]) for doc in results]

    return LoadAllOut(count=len(docs), documents=docs)