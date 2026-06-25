"""
vector_store.py
-----------------
Job: Save text chunks (as embeddings) into ChromaDB, and load them back.

Why ChromaDB?
Normal databases search by EXACT match (e.g. "find name = John").
We need to search by MEANING (e.g. "find text closest in meaning to
this question"). ChromaDB stores vectors (number-lists) and can
instantly find the closest ones using math (cosine similarity).

Analogy: every chunk is a point in space. Similar meaning = points
close together. ChromaDB finds the closest points to your question.
"""

from langchain_community.vectorstores import Chroma
from backend.embeddings import get_embedding_model
from backend.config import settings


def build_vector_store(chunks: list[str], collection_name: str):
    """
    Takes a list of text chunks, converts each to an embedding,
    and saves them into a ChromaDB collection on disk.

    A "collection" is like a labeled folder inside ChromaDB —
    we use one collection per uploaded PDF (named after the file)
    so different PDFs don't mix together.
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        collection_name=collection_name,
        persist_directory=settings.CHROMA_DIR,
    )
    return vector_store


def load_vector_store(collection_name: str):
    """
    Reconnects to an already-saved ChromaDB collection
    (used later when answering questions, so we don't
    have to re-embed the PDF every time).
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=settings.CHROMA_DIR,
    )
    return vector_store
