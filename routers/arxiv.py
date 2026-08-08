from fastapi import APIRouter, HTTPException
from schemas.arxiv import ArxivFetchIn, PaperOut, ArxivFetchOut
from fetchers.arxiv_fetch import fetch_papers
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/arxiv", tags=["arxiv"])

@router.post("/fetch")
def fetch_arxiv_papers(request: ArxivFetchIn):
    try: 
        papers = fetch_papers(request.query, request.max_results)
    except Exception as e:
        logger.error(f"Fetched endpoint failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch papers from arxiv. Try again shortly.")

    paper_objects = [PaperOut(**paper) for paper in papers]
    return ArxivFetchOut(count = len(paper_objects), papers = paper_objects)