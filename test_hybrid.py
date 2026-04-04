import sys
import os
sys.path.append(os.path.abspath("."))

from backend.memory.episodic import EpisodicMemory
from backend.retrieval.vector_store import VectorStore
from backend.retrieval.graph_store import GraphStore
from backend.retrieval.hybrid import HybridRetriever
from backend.reasoning.kg_builder import KGBuilder


# 🧠 Initialize memory
memory = EpisodicMemory()

# simulate past conversation
memory.add("What is AI?", "AI is artificial intelligence")
memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")


# 🔹 Load vector store
vs = VectorStore()
vs.load()


# 🔹 Build graph (temporary)
kg_builder = KGBuilder()
graph = GraphStore()

DATA_PATH = "data/raw"

for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            text = f.read()
            triples = kg_builder.extract_triples(text)
            graph.add_triples(triples)


# 🔥 Hybrid system (FIXED)
hybrid = HybridRetriever(vs, graph, memory)


# 🔹 Query
query = "Where is AI used?"

results = hybrid.retrieve(query)


# 🔹 Output
print("\n--- RAW RESULTS ---")
print(results)

print("\n--- FORMATTED CONTEXT ---")
context = hybrid.format_context(results)
print(context)