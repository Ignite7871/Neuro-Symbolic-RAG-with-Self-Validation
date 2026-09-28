from backend.memory.episodic import EpisodicMemory


def test_get_recent_returns_last_k_in_order():
    memory = EpisodicMemory()
    memory.add("What is AI?", "AI is artificial intelligence")
    memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")
    memory.add("What is ML?", "ML is a subset of AI")

    recent = memory.get_recent(k=2)

    assert len(recent) == 2
    assert recent[0]["query"] == "Where is AI used?"
    assert recent[1]["query"] == "What is ML?"


def test_search_matches_keyword_in_query():
    memory = EpisodicMemory()
    memory.add("What is AI?", "AI is artificial intelligence")
    memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")
    memory.add("What is the weather?", "I don't know")

    results = memory.search("AI")

    assert len(results) == 2
    assert all("AI" in r["query"] for r in results)


def test_search_returns_empty_when_no_match():
    memory = EpisodicMemory()
    memory.add("What is AI?", "AI is artificial intelligence")

    results = memory.search("weather")

    assert results == []
