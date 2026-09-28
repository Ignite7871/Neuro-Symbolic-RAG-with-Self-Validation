# Neuro-Symbolic Memory-Augmented RAG System
[![Tests](https://github.com/Ignite7871/Neuro-Symbolic-RAG-with-Self-Validation/actions/workflows/tests.yml/badge.svg)](https://github.com/Ignite7871/Neuro-Symbolic-RAG-with-Self-Validation/actions/workflows/tests.yml)

A modular Retrieval-Augmented Generation (RAG) system that combines **semantic retrieval, knowledge-graph reasoning, episodic memory, and response validation** to provide context-aware and more explainable answers.

The project explores how multiple sources of context can be combined before generation and how generated responses can be checked against structured knowledge before being returned to the user.

---

## 🧠 System Overview

The system combines four context and reasoning components:

* **Vector Retrieval** using FAISS and sentence-transformer embeddings
* **Knowledge Graph Retrieval** using extracted subject–relation–object triples
* **Episodic Memory** for previously observed query/response interactions
* **Response Validation** against structured graph knowledge

A local **Mistral model served through Ollama** is used for generation.

---

## 🏗️ Architecture

```text
                         User Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Episodic Memory   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Hybrid Retrieval  │
                  └───────┬─────┬───────┘
                          │     │
              ┌───────────┘     └────────────┐
              ▼                              ▼
     ┌─────────────────┐          ┌─────────────────┐
     │  Vector Store   │          │ Knowledge Graph │
     │     FAISS       │          │     Triples     │
     └────────┬────────┘          └────────┬────────┘
              │                            │
              └─────────────┬──────────────┘
                            ▼
                  ┌─────────────────────┐
                  │  Context Formatting │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │   Prompt Builder    │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │  Local LLM (Mistral) │
                  │       Ollama         │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Response Validator  │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Answer + Confidence │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Store in Memory     │
                  └─────────────────────┘
```

---

## 🔍 Retrieval Components

### 1. Semantic Retrieval

Documents are split into sentence-based chunks and embedded using a sentence-transformer model.

The resulting embeddings are stored in a **FAISS `IndexFlatL2`** index for nearest-neighbour retrieval.

Default embedding model:

```text
all-MiniLM-L6-v2
```

The vector store returns the top-k semantically similar chunks for a query.

---

### 2. Knowledge Graph Retrieval

The system extracts simple triples from source documents:

```text
(subject, relation, object)
```

Example:

```text
(Machine Learning, subset_of, AI)
(Deep Learning, subset_of, Machine Learning)
(AI, used_in, healthcare)
(AI, used_in, finance)
```

The current graph implementation stores these triples and retrieves those whose subject or object matches the query entity.

---

### 3. Episodic Memory

Previous interactions are stored as:

```text
{
    query,
    response,
    timestamp
}
```

The memory component supports:

* retrieving recent interactions
* keyword-based search over previous queries

This allows previously observed interactions to become part of the retrieval context.

---

### 4. Hybrid Retrieval

The `HybridRetriever` combines:

```text
Memory
+
Vector Retrieval
+
Knowledge Graph Retrieval
```

The resulting information is formatted into separate context sections before being passed to the language model.

---

## 🤖 Generation

The current implementation uses a local **Mistral model through Ollama**.

The model receives a prompt containing:

```text
Memory Context
Semantic Context
Knowledge Graph Context
Question
```

This keeps the generation pipeline independent of a remote hosted LLM API.

---

## 🛡️ Response Validation

After generation, the response is passed through a validation layer.

The current validator:

1. extracts words/entities from the generated response
2. compares them against knowledge-graph content
3. separates matching and unmatched items
4. calculates a simple confidence value from the validation results

The API returns:

```json
{
  "query": "...",
  "answer": "...",
  "confidence": 0.8,
  "invalid_claims": []
}
```

### Important limitation

The validator is currently a **rule-based prototype** rather than a general-purpose hallucination detector.

Its purpose is to demonstrate how generated responses can be checked against structured knowledge and expose potential unsupported content for further processing.

---

## 📁 Project Structure

```text
Neuro-Symbolic-RAG-with-Self-Validation/
│
├── backend/
│   ├── llm/
│   ├── memory/
│   ├── reasoning/
│   ├── retrieval/
│   ├── routes/
│   ├── config.py
│   └── main.py
│
├── scripts/
│   └── data / pipeline utilities
│
├── data/
│   └── raw/           # source .txt documents (sample_ai.txt ships as a seed)
│
├── tests/
│   └── pytest test suite
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Core Technologies

| Component                | Technology                          |
| ------------------------ | ----------------------------------- |
| Semantic embeddings      | Sentence Transformers               |
| Vector database          | FAISS                               |
| Knowledge representation | Subject–relation–object triples     |
| Memory                   | Custom episodic memory              |
| LLM                      | Mistral                             |
| Local inference          | Ollama                              |
| API                      | FastAPI                             |
| Validation               | Rule-based graph consistency checks |
| Language                 | Python                              |

---

## 🚀 Example Pipeline

Example query:

```text
Where is AI used?
```

The system can combine:

### Memory

```text
Previous interaction:
AI is used in healthcare, finance, robotics
```

### Semantic retrieval

Relevant document chunks retrieved using FAISS.

### Knowledge graph

```text
(AI, used_in, healthcare)
(AI, used_in, finance)
(AI, used_in, robotics)
```

### Generation

The retrieved context is provided to the local LLM.

### Validation

The generated answer is checked against the available graph knowledge before the API response is returned.

---

## 🔌 API

The backend exposes a `/query` endpoint.

Example request:

```http
POST /query
Content-Type: application/json
```

```json
{
  "query": "Where is AI used?"
}
```

Example response:

```json
{
  "query": "Where is AI used?",
  "answer": "AI is used in healthcare, finance, and robotics.",
  "confidence": 1.0,
  "invalid_claims": []
}
```

The exact confidence value depends on the graph contents and generated response.

---

## 🧪 Testing

The project uses `pytest` for automated testing.

The test suite covers:

* vector-store chunking and retrieval
* graph-store operations
* hybrid retrieval
* episodic memory
* response validation
* prompt construction
* LLM connection error handling

Run locally with:

```bash
pytest -v
```

GitHub Actions automatically runs the test suite on pushes and pull requests.

---

## ⚙️ Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download the NLTK sentence tokenizer (used for chunking)
python -m nltk.downloader punkt punkt_tab

# 3. Build the FAISS vector store from data/raw/*.txt
#    (a sample document ships in the repo so this works immediately;
#    run as a module so `backend` is importable)
python -m scripts.ingest_data

# 4. Start Ollama separately and pull the model referenced below, then run the API
uvicorn backend.main:app --reload
```

The service listens on `http://localhost:8000` by default; send queries to `POST /query`.

Configuration can be overridden via environment variables (see `backend/config.py`):

| Variable            | Default                                     | Purpose                              |
| ------------------- | -------------------------------------------- | ------------------------------------- |
| `DATA_PATH`          | `data/raw`                                   | Source `.txt` documents for the KG    |
| `VECTOR_STORE_PATH`  | `data/processed/vector_store`                | Saved FAISS index location            |
| `OLLAMA_URL`         | `http://localhost:11434/api/generate`        | Ollama generate endpoint              |
| `OLLAMA_MODEL`       | `mistral`                                    | Model name passed to Ollama           |

---

## 🎯 Project Goals

This project explores a modular alternative to a purely vector-based RAG pipeline by combining:

```text
Semantic Retrieval
        +
Structured Knowledge
        +
Conversation Memory
        +
LLM Generation
        +
Post-generation Validation
```

The architecture is intended as a research and engineering prototype for studying how structured and historical context can complement semantic retrieval.

---

## 🔭 Future Improvements

Potential extensions include:

* learned entity extraction instead of heuristic extraction
* graph databases such as Neo4j
* stronger claim-level validation
* retrieval evaluation metrics
* answer-faithfulness benchmarks
* configurable embedding and LLM backends
* persistent episodic memory
* Dockerized deployment
* latency and retrieval-quality benchmarking

---

## 👤 Author

**Srikar Reddy Gunupati**

B.Tech — Computer Science & Engineering (AI & ML)

Interests:

**LLMs • RAG • ML Security & Privacy • AI Reliability • Intelligent Systems**

[GitHub](https://github.com/Ignite7871)

[LinkedIn](https://linkedin.com/in/srikar-reddy-gunupati)
