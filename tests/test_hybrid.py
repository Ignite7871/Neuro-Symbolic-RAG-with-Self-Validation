from backend.retrieval.hybrid import HybridRetriever
from backend.retrieval.graph_store import GraphStore
from backend.memory.episodic import EpisodicMemory


class FakeVectorStore:
    def query(self, query_text, top_k=3):
        return [f"chunk about {query_text}"]


def _build_hybrid():
    memory = EpisodicMemory()
    memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")

    graph = GraphStore()
    graph.add_triples([
        ("AI", "used_in", "healthcare"),
        ("AI", "used_in", "finance"),
    ])

    return HybridRetriever(FakeVectorStore(), graph, memory)


def test_extract_entity_picks_capitalized_non_stopword():
    hybrid = _build_hybrid()

    assert hybrid.extract_entity("Where is AI used?") == "AI"
    assert hybrid.extract_entity("what is going on") == "what is going on"


def test_retrieve_returns_memory_vector_and_graph_results():
    hybrid = _build_hybrid()

    results = hybrid.retrieve("Where is AI used?")

    assert set(results.keys()) == {"memory", "vector", "graph"}
    assert len(results["memory"]) == 1
    assert len(results["vector"]) == 1
    assert len(results["graph"]) == 2


def test_format_context_includes_all_sections():
    hybrid = _build_hybrid()
    results = hybrid.retrieve("Where is AI used?")

    context = hybrid.format_context(results)

    assert "=== Memory Context ===" in context
    assert "=== Semantic Context ===" in context
    assert "=== Knowledge Graph Context ===" in context
