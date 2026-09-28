class HybridRetriever:
    def __init__(self, vector_store, graph_store, memory):
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.memory = memory

    def extract_entity(self, query):
        words = query.split()
        stop_words = {"What", "Where", "When", "Why", "How", "Is", "Are"}

        entities = [
            w for w in words
            if w[0].isupper() and w not in stop_words
        ]

        return " ".join(entities) if entities else query

    def retrieve(self, query, top_k=3):
        print("\n[Hybrid Retrieval + Memory]")

        # Memory search
        memory_results = self.memory.search(query)

        # Vector search
        vector_results = self.vector_store.query(query, top_k=top_k)

        # Graph search
        entity = self.extract_entity(query)
        print(f"Extracted Entity for KG: {entity}")

        graph_results = self.graph_store.query(entity)

        return {
            "memory": memory_results,
            "vector": vector_results,
            "graph": graph_results
        }

    def format_context(self, results):
        context = ""

        # Memory
        context += "=== Memory Context ===\n"
        for m in results["memory"]:
            context += f"- Q: {m['query']} | A: {m['response']}\n"

        # Vector
        context += "\n=== Semantic Context ===\n"
        for v in results["vector"]:
            context += f"- {v}\n"

        # Graph
        context += "\n=== Knowledge Graph Context ===\n"
        for (subj, rel, obj) in results["graph"]:
            context += f"- {subj} {rel} {obj}\n"

        return context