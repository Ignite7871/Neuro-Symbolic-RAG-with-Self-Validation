# Neuro-Symbolic Memory-Augmented RAG System

A hybrid AI system that combines Retrieval-Augmented Generation (RAG), Knowledge Graph reasoning, episodic memory, and a self-validation mechanism to produce reliable and explainable responses.

---

## Features

- Vector-based semantic retrieval (FAISS)
- Knowledge Graph reasoning (triples)
- Episodic memory for context awareness
- Hybrid retrieval (vector + graph)
- Local LLM (Mistral via Ollama)
- Self-validation to detect hallucinations

---

## Architecture
User Query
     ↓
Memory
     ↓
Vector Retrieval
     ↓
Knowledge Graph
     ↓
Hybrid Context
     ↓
LLM
     ↓
Validator
     ↓
Final Answer + Confidence

