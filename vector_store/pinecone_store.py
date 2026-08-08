from pinecone import Pinecone, ServerlessSpec
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)

pc = Pinecone(api_key=settings.pinecone_api_key)
INDEX_NAME = settings.pinecone_index_name

if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME) 

def bulk_upsert_hybrid(records: list[dict], namespace: str = "papers", batch_size: int = 100):
    """
    Upsert a list of records into the Pinecone index.

    Args:
        records (list[dict]): List of records to upsert.
        namespace (str): Namespace for the records in the index.
    """
    logger.info(f"Upserting {len(records)} records into Pinecone index '{INDEX_NAME}' under namespace '{namespace}'.")
    total = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        total += len(batch)
        logger.info(f"Upserted {total} records so far.")
    return total

def hybrid_search(dense_vec: list[float], sparse_vec: dict, top_k: int = 5, namespace: str = "papers", alpha: float = 0.5):
    #alpha - controls how much weight should be given to the dense vector vs the sparse vector in the hybrid search.
    #alpha = 0.0 -> BM25/keyword search only
    #alpha = 1.0 -> dense vector search only
    scaled_dense = [v * alpha for v in dense_vec] #scaling fown the vector values
    scaled_sparse = {
        "indices": sparse_vec["indices"],
        "values": [v * (1 - alpha) for v in sparse_vec["values"]],
    }

    results = index.query(
        vector = scaled_dense,
        sparse_vector = scaled_sparse,
        top_k = top_k,
        namespace = namespace,
        include_metadata = True,
    )

    return results["matches"]