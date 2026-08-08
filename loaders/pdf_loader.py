import fitz #pymupdf
from utils.logger import get_logger
import os

logger = get_logger(__name__)

def load_pdf_text(file_path: str) -> str: #to load single research paper
    try:
        doc = fitz.open(file_path)
    except Exception:
        logger.error(f"Failed to open PDF: {file_path}")
        raise

    pages_text = []

    for i, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            logger.warning(f"Page {i} in {file_path} extracted empty text.")
        pages_text.append(text)

    doc.close()
    return "\n\n".join(pages_text)


def load_all_pdfs(directory: str = "research_papers") -> list[dict]:
    """
    Loads every PDF in the given directory
    """

    results = []
    pdf_files = []

    for f in os.listdir(directory):
        if f.endswith(".pdf"):
            pdf_files.append(f)

    logger.info(f"Found {len(pdf_files)} PDFs in {directory} directory")

    for filename in pdf_files:
        file_path = os.path.join(directory, filename)
        try:
            text = load_pdf_text(file_path)
            results.append({"file_name": filename, "text": text})
            logger.info(f"Loaded: {filename} ({len(text)} characters)")
        except Exception:
            logger.exception(f"Skipping {filename} due to load failure")
            continue # one bad PDF should not stop the whole batch

    return results