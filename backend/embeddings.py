"""
embeddings.py
--------------
Job: Provide one function that gives us the "embedding model" object.

What is an embedding?
It's a list of numbers (a vector) that represents the MEANING of text.
Texts with similar meaning get similar numbers, even if the words
used are totally different.

Why GoogleGenerativeAIEmbeddings?
It's a ready-made wrapper from LangChain that calls Google's free
Gemini embedding model for us and returns clean number-vectors,
instead of us writing raw API request code ourselves.
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import settings


def get_embedding_model():
    """
    Returns an embedding model object.
    Calling .embed_query(text) or .embed_documents([texts]) on it
    will return the number-vectors for that text.
    """
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
    )
