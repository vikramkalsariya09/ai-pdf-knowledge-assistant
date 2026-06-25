"""
retriever.py
-------------
Job: Given a question, find the most relevant chunks from ChromaDB.

How it works:
1. Convert the question into an embedding (same model as the chunks).
2. ChromaDB compares this embedding against every stored chunk embedding.
3. Return the "TOP_K" closest matches (most similar in meaning).

Why top K and not all chunks?
Sending the LLM too much text is slow, costly, and can confuse it with
irrelevant info. We only want the most relevant evidence.
"""

from backend.vector_store import load_vector_store
from backend.config import settings


def retrieve_relevant_chunks(question: str, collection_name: str):
    """
    Returns a list of the most relevant chunks (as text) for the question,
    along with their similarity scores.
    """
    vector_store = load_vector_store(collection_name)

    # similarity_search_with_score returns (chunk, distance_score) pairs
    results = vector_store.similarity_search_with_score(
        query=question,
        k=settings.TOP_K,
    )

    relevant_chunks = []
    for doc, score in results:
        relevant_chunks.append({
            "text": doc.page_content,
            "similarity_score": float(score),
        })

    return relevant_chunks
