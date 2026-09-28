import os

DATA_PATH = os.environ.get("DATA_PATH", "data/raw")
VECTOR_STORE_PATH = os.environ.get("VECTOR_STORE_PATH", "data/processed/vector_store")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")
