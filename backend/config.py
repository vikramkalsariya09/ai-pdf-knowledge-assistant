"""
config.py
----------
Why this file exists:
Instead of every file calling os.getenv() separately, we load all settings
ONCE here. Other files just import from here. This is called
"centralized configuration" — a common best practice.
"""

import os
from dotenv import load_dotenv

# This line reads the .env file and loads its variables into the environment
load_dotenv()

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "storage/uploaded_pdfs")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "storage/chroma_db")

    # Settings for chunking (explained in Step 4)
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # How many chunks to retrieve per question (explained in Step 7)
    TOP_K: int = 4

    # Models (Google Gemini - free tier available)
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-2.5-flash"

settings = Settings()

# Make sure required folders exist when the app starts
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
