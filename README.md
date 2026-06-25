# 📄 AI PDF Knowledge Assistant (RAG Chatbot)

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

## 🎯 Interview Questions Based on This Project

**Q: What is RAG and why use it instead of fine-tuning?**
RAG retrieves relevant external data at query-time and feeds it to the LLM,
rather than retraining the model on new data. It's cheaper, faster to
update (just re-upload a new PDF), and reduces hallucination since the
model answers from given context rather than memory.

**Q: Why did you chunk the text instead of embedding the whole PDF at once?**
LLMs and embedding models have token limits, and large chunks reduce
retrieval precision — irrelevant text gets dragged in alongside relevant
text. Smaller, overlapping chunks give more accurate, focused retrieval.

**Q: How does the system "know" which chunks are relevant?**
It converts the question into an embedding and uses cosine similarity to
compare it against every stored chunk embedding, returning the closest
matches (smallest distance = most similar meaning).

**Q: How do you prevent the LLM from hallucinating?**
The prompt explicitly instructs the LLM to answer ONLY from the given
context, and to say "I don't know" if the answer isn't present.
Temperature is also set to 0 to reduce creative/random output.

**Q: What would you change to make this production-ready?**
Add user authentication, support multiple PDFs per user with metadata
filtering, switch ChromaDB to a hosted vector DB (e.g. Pinecone/Weaviate)
for scalability, add caching, add streaming responses, and add automated
evaluation of answer quality (RAG evaluation metrics).

**Q: What's the difference between chunk_size and chunk_overlap?**
chunk_size is how many characters go in each chunk. chunk_overlap is how
many characters are repeated between consecutive chunks, so an idea split
across a chunk boundary isn't lost entirely from either chunk.

**Q: Why use a vector database instead of just keyword search?**
Keyword search needs exact word matches ("car" won't match "automobile").
Vector search compares meaning, so it finds relevant content even when
the wording is completely different from the question.

---

## 🔧 Possible Extensions (Good Talking Points for Interviews)
- Support multiple PDFs and let users pick which one to query
- Add chat memory (multi-turn conversations that reference earlier questions)
- Add streaming token-by-token answers in the UI
- Swap OpenAI for a local open-source LLM (e.g. via Ollama)
- Add OCR support for scanned PDFs
- Deploy backend on Render/Railway and frontend on Streamlit Cloud
