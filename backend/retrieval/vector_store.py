from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import nltk
from nltk.tokenize import sent_tokenize

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.text_chunks = []

    def create_chunks(self, text, chunk_size=300, overlap=1):
        sentences = sent_tokenize(text)

        chunks = []
        current_chunk = []

        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            if current_length + sentence_length > chunk_size:
                chunks.append(" ".join(current_chunk))

            # overlap (keep last sentence)
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_length = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += sentence_length

            if current_chunk:
                chunks.append(" ".join(current_chunk))

        return chunks

    def build_index(self, documents):
        print("Creating chunks...")
        all_chunks = []

        for doc in documents:
            chunks = self.create_chunks(doc)
            all_chunks.extend(chunks)

        self.text_chunks = all_chunks

        print(f"Total chunks: {len(all_chunks)}")

        print("Generating embeddings...")
        embeddings = self.model.encode(all_chunks)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        print("Building FAISS index...")
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        print("Index built successfully!")

    def save(self, path="data/processed/vector_store"):
        os.makedirs(path, exist_ok=True)

        faiss.write_index(self.index, f"{path}/index.faiss")

        with open(f"{path}/chunks.pkl", "wb") as f:
            pickle.dump(self.text_chunks, f)

        print("Vector store saved!")

    def load(self, path="data/processed/vector_store"):
        print("Loading index...")
        self.index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/chunks.pkl", "rb") as f:
            self.text_chunks = pickle.load(f)

        print("Vector store loaded!")

    def query(self, query_text, top_k=3):
        print(f"\nQuery: {query_text}")

        query_embedding = self.model.encode([query_text]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = [self.text_chunks[i] for i in indices[0]]

        return results