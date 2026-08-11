def build_rag_prompt(query: str, chunks: list[dict]) -> str:
    context_blocks = [
        f"[Source {i+1}: {c['title']} by {c['authors']}]\n{c['text']}"
        for i, c in enumerate(chunks)
    ] #top_k retrieved chunks
    context = "\n\n".join(context_blocks)

    prompt = f"""You are a research assistant that answers questions strictly based on provided sources.
    Rules:
    1. Answer using ONLY the information in the context below. Do not user any outside knowledge.
    2. Every claim must be followed by a citation in [Source N] format.
    3. If a claim has no supporting source, do not include it.
    4. If the context does not contain enough information to answer the question , respond exactly with:
       "I don't have enough information in the provided sources to answer this.
    5. Do not guess or fill gaps with assumptions.

    Context:
    {context}

    Question: {query}

    Answer (with citation):"""

    return prompt