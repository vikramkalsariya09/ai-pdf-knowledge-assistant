"""
main.py
--------
This is the FastAPI app — the "control center" that ties together
every piece we built: pdf_reader, chunker, vector_store, retriever, llm.

It exposes two simple endpoints:
1. POST /upload-pdf   -> upload a PDF, process it, store it in ChromaDB
2. POST /ask          -> ask a question about an already-uploaded PDF

Why FastAPI?
It's fast to write, auto-generates interactive docs (at /docs),
and validates incoming data for us automatically.
"""

import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.config import settings
from backend.pdf_reader import extract_text_from_pdf
from backend.chunker import split_text_into_chunks
from backend.vector_store import build_vector_store
from backend.retriever import retrieve_relevant_chunks
from backend.llm import generate_answer
from utils.helpers import make_collection_name

app = FastAPI(title="AI PDF Knowledge Assistant")


class AskRequest(BaseModel):
    question: str
    collection_name: str


@app.get("/")
def health_check():
    """Simple endpoint to confirm the server is running."""
    return {"status": "ok", "message": "AI PDF Knowledge Assistant backend is running"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    STEP-BY-STEP what happens when a PDF is uploaded:
    1. Save the uploaded file to disk
    2. Extract its text       (pdf_reader.py)
    3. Split text into chunks (chunker.py)
    4. Embed + store chunks   (vector_store.py)
    5. Return the collection_name so the frontend can use it later
       when asking questions about THIS specific PDF.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 1. Save the uploaded file to disk
    save_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Extract text
    raw_text = extract_text_from_pdf(save_path)
    if not raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text found. This PDF might be a scanned image.",
        )

    # 3. Split into chunks
    chunks = split_text_into_chunks(raw_text)

    # 4. Embed + store in ChromaDB
    collection_name = make_collection_name(file.filename)
    build_vector_store(chunks, collection_name)

    return {
        "message": "PDF processed and stored successfully.",
        "filename": file.filename,
        "collection_name": collection_name,
        "num_chunks": len(chunks),
    }


@app.post("/ask")
async def ask_question(request: AskRequest):
    """
    STEP-BY-STEP what happens when a question is asked:
    1. Retrieve the most relevant chunks from ChromaDB (retriever.py)
    2. Send question + chunks to the LLM                (llm.py)
    3. Return the answer AND the source chunks used,
       so the user can verify where the answer came from.
    """
    relevant_chunks = retrieve_relevant_chunks(
        question=request.question,
        collection_name=request.collection_name,
    )

    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant content found. Did you upload the PDF first?",
        )

    answer = generate_answer(request.question, relevant_chunks)

    return {
        "question": request.question,
        "answer": answer,
        "source_chunks": relevant_chunks,
    }
