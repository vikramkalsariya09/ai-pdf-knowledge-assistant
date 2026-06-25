# 📄 AI PDF Knowledge Assistant (RAG Chatbot)

🔗 **Live Demo:** https://ai-pdf-knowledge-assistant-hjfw8sxthceckmqemzxwex.streamlit.app
🔗 **Backend API Docs:** https://ai-pdf-knowledge-assistant-vmd3.onrender.com/docs

> Note: The backend is hosted on Render's free tier, which sleeps after
> 15 minutes of inactivity. The first request after a period of inactivity
> may take 30-50 seconds to respond while the server wakes up.

A beginner-friendly RAG (Retrieval-Augmented Generation) chatbot that lets you
upload a PDF and ask questions about its content. Answers are grounded in the
actual document — not the LLM's general knowledge — and every answer shows
the source chunks it was based on.

---

## 🏗 Project Structure

```
ai-pdf-assistant/
├── backend/
│   ├── main.py            # FastAPI app — API endpoints
│   ├── config.py          # Central settings (API keys, paths, model names)
│   ├── pdf_reader.py       # PDF -> raw text
│   ├── chunker.py          # raw text -> small overlapping chunks
│   ├── embeddings.py       # text -> embedding model wrapper
│   ├── vector_store.py     # save/load embeddings in ChromaDB
│   ├── retriever.py        # find relevant chunks for a question
│   └── llm.py              # build prompt, call LLM, return answer
├── frontend/
│   └── app.py              # Streamlit chat UI
├── utils/
│   └── helpers.py          # small shared helper functions
├── storage/
│   ├── uploaded_pdfs/       # saved PDF uploads
│   └── chroma_db/           # ChromaDB's persisted vector data
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ How It Works (RAG Pipeline)

```
PDF Upload
   ↓
Extract text (pypdf)
   ↓
Split into chunks (LangChain text splitter)
   ↓
Convert chunks to embeddings (Google Gemini embedding model)
   ↓
Store embeddings in ChromaDB
   ↓
[User asks a question]
   ↓
Convert question to embedding
   ↓
ChromaDB finds the most similar chunks ("Retrieval")
   ↓
Send question + chunks to LLM ("Augmented Generation")
   ↓
LLM answers using ONLY the given chunks
   ↓
Answer + source chunks shown to user
```

---

## 🚀 Setup & Run Instructions

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key (FREE - Google Gemini)
```bash
cp .env.example .env
```
Get a free key from `https://aistudio.google.com/app/apikey` (no credit card
needed), then open `.env` and paste it into `GOOGLE_API_KEY=`.

### 4. Run the backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
Visit `http://127.0.0.1:8000/docs` to see the interactive API docs.

### 5. Run the frontend (Streamlit) — in a NEW terminal
```bash
streamlit run frontend/app.py
```
This opens a browser tab where you can upload a PDF and start chatting.

### 6. Test it
1. Upload any text-based PDF (not a scanned image).
2. Click "Process PDF" and wait for the success message.
3. Type a question that the PDF should answer.
4. Read the answer, then expand "Show source chunks" to see the
   exact text the answer was grounded in.

---

## 📚 Key Concepts Explained Simply

**RAG (Retrieval-Augmented Generation)**
Instead of asking an LLM to answer purely from what it memorized during
training, we first *retrieve* the actual relevant text from your document,
then ask the LLM to *generate* an answer using only that text. This reduces
made-up answers (hallucinations) and lets the AI answer about documents it
has never seen before.

**Embeddings**
A way of converting text into a list of numbers that represents its
*meaning*. Texts with similar meaning get similar numbers, even if the
wording is completely different.

**Chunking**
Splitting a long document into smaller pieces before processing. This is
necessary because LLMs have a limited context window, and smaller pieces
make retrieval more precise (less irrelevant text gets pulled in).

**Vector Database (ChromaDB)**
A database designed to store embeddings and search them by similarity of
meaning, instead of exact keyword matches. It can instantly find "the
chunks most similar to this question" using math (cosine similarity).

---

