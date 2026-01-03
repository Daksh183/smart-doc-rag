# Smart Document Search & Question Answering System (RAG)

This project is a **document-grounded Question Answering system** built using the
**Retrieval-Augmented Generation (RAG)** approach.

The system allows a user to:
- Upload a PDF document
- Ask natural language questions
- Get answers **only from the content of the document**

If the information is not present in the document, the system explicitly refuses to answer.

---

## 🔍 Why this project exists

Large Language Models (LLMs) by default:
- Hallucinate answers
- Use their pretrained world knowledge
- Cannot be trusted for private or document-specific data

This project solves that problem by:
1. Retrieving relevant document chunks using semantic search
2. Calling the LLM **only when retrieval confidence is sufficient**
3. Blocking answers when the document does not support the query

This enforces **document grounding at the system level**, not just via prompts.

---

## ⚙️ How it works (High-level)

PDF
→ Text Extraction
→ Text Chunking
→ Embedding Generation
→ FAISS Vector Index
→ Similarity Search
→ LLM Answer Generation

yaml
Copy code

Each step is implemented explicitly without using frameworks like LangChain,
to keep the system transparent and debuggable.

---

## 🏗️ Architecture Components

### 1. PDF Processing
- Extracts raw text from PDF using PyMuPDF
- Handles multi-page documents

### 2. Text Chunking
- Splits text into overlapping chunks
- Improves retrieval accuracy
- Prevents token-limit issues

### 3. Embeddings & Retrieval
- Uses SentenceTransformers (`all-MiniLM-L6-v2`)
- FAISS IndexFlatIP for cosine-similarity search
- Retrieves top-k most relevant chunks

### 4. Hard Retrieval Gate
- If no chunk passes similarity filtering → **LLM is not called**
- Prevents hallucinations by design

### 5. Answer Generation
- Uses a local LLM via Ollama
- Prompted to rephrase answers naturally
- Cannot introduce external knowledge if gating blocks it

---

## 🛠️ Tech Stack

- Python
- PyMuPDF (PDF text extraction)
- SentenceTransformers (embeddings)
- FAISS (vector similarity search)
- Ollama (local LLM inference)

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Start Ollama and pull the model
bash
Copy code
ollama pull llama3.1:8b
3. Run the system
bash
Copy code
python main.py
📌 Example Interaction
vbnet
Copy code
Ask your question: What is the capital of France?
Answer: The capital of France is Paris.

Ask your question: What is the capital of India?
Answer: Not found in the document.
⚠️ Key Design Decisions
No model training — focus on system design

Simple chunking for clarity

Exact FAISS search for correctness

Prompt used for style, not correctness

Hallucination prevention handled in code, not by the LLM

🔮 Future Improvements
FastAPI backend for web access

Source citations (page / section)

Persistent FAISS index

Better semantic chunking

