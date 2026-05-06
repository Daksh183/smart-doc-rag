# Smart Doc RAG

A local question-answering system that lets you ask questions about any PDF — and only answers from what's actually in it.

No hallucinations. No guessing. If the document doesn't have the answer, it says so.

---

## What it does

You point it at a PDF, ask a question in plain English, and it finds the most relevant parts of the document and uses a local LLM to give you a clean, natural answer. The key thing is that the LLM is only called if the retrieval step actually finds something relevant — so it can't make things up.

Built without LangChain or any high-level RAG framework, so every step is explicit and easy to follow.

---

## How it works

```
PDF → Text Extraction → Chunking → Embeddings → FAISS Index → Similarity Search → LLM Answer
```

1. **PDF Processing** — extracts raw text from the PDF using PyMuPDF, page by page
2. **Chunking** — splits the text into overlapping chunks (500 chars, 100 overlap) so context isn't lost at boundaries
3. **Embeddings** — converts each chunk into a vector using `all-MiniLM-L6-v2` from SentenceTransformers
4. **FAISS Index** — stores those vectors in a FAISS flat index using cosine similarity (inner product on normalized vectors)
5. **Retrieval Gate** — searches the index for the top-k most relevant chunks; if nothing clears the similarity threshold, the LLM is never called
6. **Answer Generation** — passes the retrieved chunks as context to a local LLM via Ollama, which rephrases the answer naturally without adding anything outside the document

---

## Tech stack

- **PyMuPDF** — PDF text extraction
- **SentenceTransformers** — `all-MiniLM-L6-v2` for embeddings
- **FAISS** — vector similarity search
- **Ollama** — local LLM inference (`llama3.1:8b`)
- **Python** — no frameworks, just the pipeline

---

## Getting started

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Pull the model via Ollama**
```bash
ollama pull llama3.1:8b
```
Make sure Ollama is running before the next step (`ollama serve` if it isn't).

**3. Drop your PDF in the project folder and update the path in `main.py`**
```python
pdf_path = "your_document.pdf"
```

**4. Run it**
```bash
python main.py
```

---

## Example

```
Ask your question (or type 'exit' to quit): What is the refund policy?

Answer: According to the document, refunds are processed within 7 business days...

Ask your question (or type 'exit' to quit): Who is the CEO of Apple?

No relevant information found in the document.
```

---

## Design decisions worth noting

- **No LangChain** — every step is written explicitly so you can see exactly what's happening and debug it easily
- **Retrieval gate** — hallucination prevention is enforced in code, not just via prompt instructions. If retrieval fails, the LLM doesn't run
- **Local LLM** — everything runs on your machine, no API keys, no data leaving your system
- **Cosine similarity via FAISS** — embeddings are L2-normalized so inner product search behaves like cosine similarity

---

## What's next

- FastAPI backend so it can be used as a web service
- Source citations (page number, section)
- Persistent FAISS index so you don't re-embed on every run
- Smarter semantic chunking instead of fixed-size sliding window
