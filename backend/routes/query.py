from fastapi import APIRouter
from pydantic import BaseModel

from backend.memory.episodic import EpisodicMemory
from backend.retrieval.vector_store import VectorStore
from backend.retrieval.graph_store import GraphStore
from backend.retrieval.hybrid import HybridRetriever
from backend.reasoning.kg_builder import KGBuilder
from backend.llm.model import LLM
from backend.llm.prompt import build_prompt
from backend.reasoning.validator import Validator
from backend.config import DATA_PATH

import os

router = APIRouter()

# Request schema
class QueryRequest(BaseModel):
    query: str


# Initialize system (load once, at import time)
memory = EpisodicMemory()
vs = VectorStore()
vs.load()

kg_builder = KGBuilder()
graph = GraphStore()

os.makedirs(DATA_PATH, exist_ok=True)

for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            text = f.read()
            triples = kg_builder.extract_triples(text)
            graph.add_triples(triples)

if not graph.get_all():
    print(f"Warning: no knowledge graph triples loaded from '{DATA_PATH}'. "
          f"Add .txt documents there and rerun scripts/ingest_data.py.")

hybrid = HybridRetriever(vs, graph, memory)
llm = LLM()
validator = Validator(graph)


# API endpoint
@router.post("/query")
def query_system(request: QueryRequest):
    query = request.query

    # Retrieve
    results = hybrid.retrieve(query)
    context = hybrid.format_context(results)

    # Build prompt
    prompt = build_prompt(query, context)

    # Generate
    response = llm.generate(prompt)

    # Validate
    validation = validator.validate(response)

    # Store in memory
    memory.add(query, response)

    return {
        "query": query,
        "answer": response,
        "confidence": validation["confidence"],
        "invalid_claims": validation["invalid"]
    }