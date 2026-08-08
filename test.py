from embeddings.embedder import embed_dense, fit_bm25, embed_sparse, embed_sparse_query
from services.ingestion import process_all_papers
from vector_store.pinecone_store import bulk_upsert_hybrid, hybrid_search

known_text = """Cats are small domesticated animals that enjoy sleeping and chasing mice. They are known for their independence and agility.

Dogs are loyal companions known for their loud barking and playful energy. They require regular exercise and social interaction.

Seiberg duality relates two different gauge theories that describe the same underlying physics. This concept is important in theoretical physics.

Quiver gauge theories are studied using mutation trees and duality cascades. Researchers use machine learning to trace these relationships."""

chunks = process_all_papers("research_papers")
one_paper_chunks = [c for c in chunks if c['source'] == "2607.28271v1"]
texts = [c['text'] for c in one_paper_chunks]


fit_bm25(texts, save_path="test_bm25.json")

dense_vectors = embed_dense(texts)
sparse_vectors = embed_sparse(texts)

for c in one_paper_chunks:
    if "paragraphs_hit" in c['text']:
        print(c['id'], len(c['text']), "\n", c['text'], "\n---")

records = [
    {
        "id": c["id"],
        "values": dense_vec,
        "sparse_values": sparse_vec,
        "metadata": {
            "text": c["text"],
            "source": c["source"],
            "title": c["title"],
            "authors": c["authors"],
            "published": c["published"],
        },
    }

    for c, dense_vec, sparse_vec in zip(one_paper_chunks, dense_vectors, sparse_vectors)
]

count = bulk_upsert_hybrid(records, namespace="papers", batch_size=100)
print(f"Upserted {count} records into Pinecone")

query = "What evaluation metrics were used to prove the migration was correct?"

query_dense = embed_dense([query])[0]
query_sparse = embed_sparse_query(query)

for alpha in [1.0, 0.5, 0.0]:
    print(f"alpha = {alpha}")
    results = hybrid_search(query_dense, query_sparse, top_k=5, namespace="papers", alpha=alpha)
    for match in results:
        print(f"score = { match['score']:.4f} | {match['metadata']['text']}")
    print()



# # Test dense embedding
# dense_vecs = embed_dense(sample_texts)
# print(f"Dense vector count: {len(dense_vecs)}, dimension: {len(dense_vecs[0])}")

# # Test BM25 fit + document encoding
# fit_bm25(sample_texts, save_path="test_bm25.json")
# sparse_vecs = embed_sparse(sample_texts)
# print(f"Sparse vector count: {len(sparse_vecs)}")
# print(f"Sample sparse vector: {sparse_vecs[0]}")

# # Test query encoding
# query_sparse = embed_sparse_query("What is Seiberg duality?")
# print(f"Query sparse vector: {query_sparse}")