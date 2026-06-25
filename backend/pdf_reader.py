"""
pdf_reader.py
--------------
Job: Take a PDF file path -> return the raw text inside it.

Why pypdf?
PDFs store text along with layout/formatting info. pypdf knows how to
open a PDF, go page-by-page, and pull out just the text content.
"""

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Reads a PDF file and returns all its text as a single string.

    Args:
        pdf_path: full path to the PDF file on disk

    Returns:
        A single string containing text from every page,
        with page breaks marked for clarity.
    """
    reader = PdfReader(pdf_path)
    full_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""  # some pages can be empty/scanned
        full_text.append(page_text)

    return "\n".join(full_text)
