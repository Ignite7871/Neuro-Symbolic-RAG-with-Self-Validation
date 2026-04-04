from backend.retrieval.vector_store import VectorStore

vs = VectorStore()
vs.load()

queries = [
    "What is AI?",
    "Explain machine learning",
    "Where is AI used?"
]

for q in queries:
    results = vs.query(q)

    print("\nTop Results:")
    for i, res in enumerate(results):
        print(f"{i+1}. {res}")