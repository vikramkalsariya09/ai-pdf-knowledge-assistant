"""
llm.py
-------
Job: Send the question + retrieved chunks to the LLM, get back an answer.

This is the "Generation" part of RAG (Retrieval-Augmented Generation).

Why instruct the LLM to "only use the given context"?
Without this instruction, the LLM might answer from its own general
training knowledge instead of your actual PDF — this is called
"hallucination". We want the answer grounded strictly in the document.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import settings


PROMPT_TEMPLATE = """You are a helpful assistant that answers questions
using ONLY the context provided below, which comes from a PDF document.

Rules:
- If the answer is not present in the context, say:
  "I couldn't find this information in the document."
- Do not make up information.
- Keep your answer clear and concise.

Context:
{context}

Question: {question}

Answer:"""


def generate_answer(question: str, relevant_chunks: list[dict]) -> str:
    """
    Builds a prompt from the retrieved chunks + question,
    sends it to the LLM, and returns the generated answer text.
    """
    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,  # 0 = focused/factual answers, less "creative" randomness
    )

    # Join all retrieved chunk texts into one context block
    context_text = "\n\n---\n\n".join(chunk["text"] for chunk in relevant_chunks)

    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)

    response = llm.invoke(prompt)
    return response.content
