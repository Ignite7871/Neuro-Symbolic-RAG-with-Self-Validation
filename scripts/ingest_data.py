import os
from backend.retrieval.vector_store import VectorStore
from backend.config import DATA_PATH

def load_documents():
    documents = []

    if not os.path.isdir(DATA_PATH):
        print(f"No such directory: '{DATA_PATH}'")
        return documents

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)

        if file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append(f.read())

    return documents


if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents()

    if not docs:
        print("No documents found!")
        exit()

    vs = VectorStore()

    print("Building vector store...")
    vs.build_index(docs)

    print("Saving vector store...")
    vs.save()

    print("Done!")