from utils.logger import get_logger
from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder
from config import settings

logger = get_logger(__name__)

_dense_model = SentenceTransformer(settings.embedding_model_name)
_bm25 = BM25Encoder()
_bm25_fitted = False

def embed_dense(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of texts using the dense embedding model.

    Args:
        texts (list[str]): List of texts to embed.

    Returns:
        list[list[float]]: List of embeddings.
    """
    logger.info(f"Embedding {len(texts)} texts using dense model.")
    return _dense_model.encode(texts).tolist()

def fit_bm25(texts: list[str], save_path: str = "bm25_research_papers.json"):
    """
    Fit the BM25 model on a list of texts and save the fitted model to a file.
    """
    global _bm25_fitted
    logger.info(f"Fitting BM25 model on {len(texts)} texts.")
    _bm25.fit(texts)
    _bm25.dump(save_path)
    _bm25_fitted = True
    logger.info(f"BM25 model fitted and saved to {save_path}.")

def load_bm25(path: str = "bm25_research_papers.json"):
    """
    Load a fitted BM25 model from a file.
    """
    global _bm25_fitted
    logger.info(f"Loading BM25 model from {path}.")
    _bm25.load(path)
    _bm25_fitted = True
    logger.info("BM25 model loaded successfully.")

def embed_sparse(text: list[str]) -> list[dict]:
    if not _bm25_fitted:
        raise RuntimeError("BM25 model is not fitted. Please fit the model first.")
    return _bm25.encode_documents(text)

def embed_sparse_query(text: str) -> dict:
    if not _bm25_fitted:
        raise RuntimeError("BM25 model is not fitted. Please fit the model first.")
    return _bm25.encode_queries(text)