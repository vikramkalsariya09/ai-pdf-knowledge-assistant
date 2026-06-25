"""
chunker.py
-----------
Job: Take a big block of text -> split it into small overlapping chunks.

Why chunk?
1. LLMs can only "read" a limited amount of text at once (context window).
2. Smaller chunks make retrieval more precise — we only pull in the
   small piece of text that's actually relevant to the question.

Why overlap?
If we cut text at hard boundaries, we might slice an idea in half.
Overlapping the chunks (sharing some text between consecutive chunks)
keeps the meaning continuous.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.config import settings


def split_text_into_chunks(text: str):
    """
    Splits raw text into a list of chunk strings.

    RecursiveCharacterTextSplitter tries to split at natural boundaries
    in this priority order: paragraphs -> sentences -> words -> characters.
    This avoids cutting sentences awkwardly in half.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)
    return chunks
