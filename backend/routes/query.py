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

import os

router = APIRouter()

# 🧠 Request Schema
class QueryRequest(BaseModel):
    query: str


# 🔥 Initialize system (LOAD ONCE)
memory = EpisodicMemory()
vs = VectorStore()
vs.load()

kg_builder = KGBuilder()
graph = GraphStore()

DATA_PATH = "data/raw"

for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            text = f.read()
            triples = kg_builder.extract_triples(text)
            graph.add_triples(triples)

hybrid = HybridRetriever(vs, graph, memory)
llm = LLM()
validator = Validator(graph)


# 🚀 API Endpoint
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