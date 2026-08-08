from loaders.pdf_loader import load_all_pdfs
from preprocessing.cleaner import clean_text
from preprocessing.chunker import chunk_text
from utils.logger import get_logger
import os
import json

logger = get_logger(__name__)

def load_paper_metadata(arxiv_id: str, directory: str) -> dict:
    """ Reads the sidecar metadata JSON for a given paper, if it exists"""

    meta_path = os.path.join(directory, f"{arxiv_id}.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    logger.warning(f"No metadata found for {arxiv_id}, using defaults")
    return {"title": "Unknown", "authors": [], "abstract": "", "published": "Unknown", "categories": []}

def process_all_papers(directory: str = "research_papers") -> list[dict]:
    """
    Full pipeline: load -> clean -> chunk.
    """

    documents = load_all_pdfs(directory)
    all_chunks = []

    for doc in documents:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)

        arxiv_id = doc["file_name"].replace(".pdf","")
        meta = load_paper_metadata(arxiv_id, directory)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{arxiv_id}_{i}",
                "text": chunk,
                "source": arxiv_id,
                "title": meta.get("title", "Unknown"),
                "abstract": meta.get("abstract", ""),
                "authors": ", ".join(meta.get("authors", [])),
                "published": meta.get("published", "Unknown"),
                "categories": meta.get("categories", []),
            })

    logger.info(f"Processed {len(documents)} papers into {len(all_chunks)} chunks")
    return all_chunks