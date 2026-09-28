from backend.retrieval.graph_store import GraphStore


def test_add_triples_and_get_all():
    graph = GraphStore()

    graph.add_triples([
        ("AI", "used_in", "healthcare"),
        ("AI", "used_in", "finance"),
    ])

    assert len(graph.get_all()) == 2


def test_query_matches_subject():
    graph = GraphStore()

    graph.add_triples([
        ("AI", "used_in", "healthcare"),
        ("Machine Learning", "subset_of", "AI"),
    ])

    results = graph.query("AI")

    assert len(results) == 2


def test_query_matches_object():
    graph = GraphStore()

    graph.add_triples([
        ("AI", "used_in", "healthcare"),
        ("AI", "used_in", "finance"),
    ])

    results = graph.query("finance")

    assert len(results) == 1
    assert results[0] == ("AI", "used_in", "finance")


def test_query_returns_empty_for_unknown_entity():
    graph = GraphStore()

    graph.add_triples([
        ("AI", "used_in", "healthcare"),
    ])

    assert graph.query("quantum") == []
