from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from backend.config import DATA_PATH
from backend.llm.model import LLM
from backend.memory.episodic import EpisodicMemory
from backend.reasoning.kg_builder import KGBuilder
from backend.reasoning.validator import Validator
from backend.retrieval.graph_store import GraphStore
from backend.retrieval.hybrid import HybridRetriever
from backend.retrieval.vector_store import VectorStore
from backend.routes.query import router


def initialize_system():
    """Initialize all RAG components once during application startup."""

    # Memory
    memory = EpisodicMemory()

    # Vector store
    vector_store = VectorStore()
    vector_store.load()

    # Knowledge graph
    graph = GraphStore()
    kg_builder = KGBuilder()

    os.makedirs(DATA_PATH, exist_ok=True)

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_PATH, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                document = file.read()

            triples = kg_builder.extract_triples(document)
            graph.add_triples(triples)

    if not graph.get_all():
        print(
            f"Warning: no knowledge graph triples loaded from "
            f"'{DATA_PATH}'. Add .txt documents there."
        )

    # Hybrid retrieval
    hybrid = HybridRetriever(
        vector_store=vector_store,
        graph_store=graph,
        memory=memory,
    )

    # LLM
    llm = LLM()

    # Validator
    validator = Validator(graph)

    return {
        "memory": memory,
        "vector_store": vector_store,
        "graph": graph,
        "hybrid": hybrid,
        "llm": llm,
        "validator": validator,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources during startup."""

    print("Initializing Neuro-Symbolic RAG system...")

    app.state.rag = initialize_system()

    print("RAG system initialized successfully.")

    yield

    print("Shutting down Neuro-Symbolic RAG system...")


app = FastAPI(
    title="Neuro-Symbolic RAG System",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "AI System is running"}
