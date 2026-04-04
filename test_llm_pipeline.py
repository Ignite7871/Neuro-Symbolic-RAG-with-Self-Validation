import sys
import os
sys.path.append(os.path.abspath("."))

from backend.memory.episodic import EpisodicMemory
from backend.retrieval.vector_store import VectorStore
from backend.retrieval.graph_store import GraphStore
from backend.retrieval.hybrid import HybridRetriever
from backend.reasoning.kg_builder import KGBuilder
from backend.llm.model import LLM
from backend.llm.prompt import build_prompt
from backend.reasoning.validator import Validator


# 🧠 1. Initialize Memory
memory = EpisodicMemory()

memory.add("What is AI?", "AI is artificial intelligence")
memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")


# 🔍 2. Load Vector Store
vs = VectorStore()
vs.load()


# 🧩 3. Build Knowledge Graph
kg_builder = KGBuilder()
graph = GraphStore()

DATA_PATH = "data/raw"

for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            text = f.read()
            triples = kg_builder.extract_triples(text)
            graph.add_triples(triples)


# 🔥 4. Initialize Hybrid Retriever
hybrid = HybridRetriever(vs, graph, memory)


# 🤖 5. Initialize Local LLM (Ollama)
llm = LLM()


# 🛡️ 6. Initialize Validator
validator = Validator(graph)


# ❓ 7. User Query
query = "Where is AI used?"


# 🔄 8. Retrieve Context
results = hybrid.retrieve(query)
context = hybrid.format_context(results)

print("\n--- CONTEXT SENT TO LLM ---")
print(context)


# 🧠 9. Build Prompt
prompt = build_prompt(query, context)


# 🤖 10. Generate Response
# response = llm.generate(prompt)
response = "AI is used in agriculture and finance"


# ✅ 11. Final Output
print("\n=== FINAL RESPONSE ===")
print(response)


# 🛡️ 12. Validate Response (NEW 🔥)
validation = validator.validate(response)

print("\n=== VALIDATION RESULT ===")
print(validation)