"""
app.py (Streamlit Frontend)
-----------------------------
This file does NOT do any AI work itself. It only:
1. Shows a PDF upload box -> sends the file to our FastAPI backend
2. Shows a chat box -> sends the question to our FastAPI backend
3. Displays the backend's answer + source chunks

This separation (frontend never touches AI logic directly) is good
practice: it means we could swap Streamlit for a React app later
without changing any AI/backend code at all.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI PDF Knowledge Assistant", page_icon="📄")
st.title("📄 AI PDF Knowledge Assistant")
st.caption("Upload a PDF, then ask questions about it — answers are grounded in your document (RAG).")

# We use st.session_state to "remember" things between reruns of the script,
# since Streamlit re-runs the whole file on every interaction.
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- PDF UPLOAD ----------
st.subheader("1. Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None and st.button("Process PDF"):
    with st.spinner("Reading PDF, chunking, and creating embeddings..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/upload-pdf", files=files)

    if response.status_code == 200:
        data = response.json()
        st.session_state.collection_name = data["collection_name"]
        st.success(f"Done! Created {data['num_chunks']} chunks from '{data['filename']}'.")
    else:
        st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")

# ---------- CHAT ----------
st.subheader("2. Ask a question")

if st.session_state.collection_name is None:
    st.info("Upload and process a PDF first.")
else:
    question = st.text_input("Your question:")

    if st.button("Ask") and question.strip():
        with st.spinner("Searching the document and generating an answer..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "question": question,
                    "collection_name": st.session_state.collection_name,
                },
            )

        if response.status_code == 200:
            data = response.json()
            st.session_state.chat_history.append(data)
        else:
            st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")

    # Show chat history, most recent first
    for entry in reversed(st.session_state.chat_history):
        st.markdown(f"**Q: {entry['question']}**")
        st.markdown(f"**A:** {entry['answer']}")

        with st.expander("Show source chunks used for this answer"):
            for i, chunk in enumerate(entry["source_chunks"], start=1):
                st.markdown(f"**Source {i}** (distance score: {chunk['similarity_score']:.4f})")
                st.text(chunk["text"][:500] + ("..." if len(chunk["text"]) > 500 else ""))

        st.divider()
