import os
from backend.reasoning.kg_builder import KGBuilder
from backend.retrieval.graph_store import GraphStore

DATA_PATH = "data/raw"

def load_documents():
    docs = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())

    return docs


if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents()

    kg_builder = KGBuilder()
    graph = GraphStore()

    print("Extracting triples...")

    for doc in docs:
        triples = kg_builder.extract_triples(doc)

        for t in triples:
            print("Triple:", t)

        graph.add_triples(triples)

    print("\nAll triples stored:")
    for t in graph.get_all():
        print(t)

    print("\nQuery Test:")
    results = graph.query("AI")

    for r in results:
        print(r)