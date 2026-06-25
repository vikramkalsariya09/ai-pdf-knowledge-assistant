"""
helpers.py
-----------
Small reusable functions shared across the backend.
Keeping these separate avoids repeating code in main.py.
"""

import re
import os


def make_collection_name(filename: str) -> str:
    """
    ChromaDB collection names must be simple (letters, numbers, _, -).
    This converts an uploaded filename like "My Notes (1).pdf"
    into a safe collection name like "my_notes_1_pdf".
    """
    name = os.path.splitext(filename)[0]  # remove .pdf extension
    name = name.lower()
    name = re.sub(r"[^a-z0-9_-]", "_", name)
    return name
