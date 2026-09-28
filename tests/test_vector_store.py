from backend.retrieval.vector_store import VectorStore


def test_create_chunks_groups_sentences_without_duplication():
    # Skip __init__ so this doesn't need the embedding model installed/downloaded.
    vs = VectorStore.__new__(VectorStore)

    text = (
        "AI is a subset of Computer Science. "
        "Machine Learning is a subset of AI. "
        "Deep Learning is a subset of Machine Learning. "
        "AI is used in healthcare, finance, and robotics."
    )

    # Regression test: the old implementation flushed a chunk on every single
    # loop iteration regardless of size, so each sentence ended up alone (and
    # duplicated) instead of being grouped up to chunk_size.
    chunks = vs.create_chunks(text, chunk_size=100, overlap=0)

    assert len(chunks) == 2
    assert "AI is a subset of Computer Science" in chunks[0]
    assert "Machine Learning is a subset of AI" in chunks[0]
    assert "Deep Learning is a subset of Machine Learning" in chunks[1]
    assert "AI is used in healthcare" in chunks[1]
    # no sentence duplicated when overlap is disabled
    assert "".join(chunks).count("AI is a subset of Computer Science") == 1


def test_create_chunks_overlap_repeats_boundary_sentence():
    vs = VectorStore.__new__(VectorStore)

    text = (
        "AI is a subset of Computer Science. "
        "Machine Learning is a subset of AI. "
        "Deep Learning is a subset of Machine Learning. "
        "AI is used in healthcare, finance, and robotics."
    )

    chunks = vs.create_chunks(text, chunk_size=100, overlap=1)

    assert len(chunks) == 3
    # the boundary sentence should be carried into the next chunk (sliding window)
    assert "Machine Learning is a subset of AI" in chunks[0]
    assert "Machine Learning is a subset of AI" in chunks[1]


def test_build_index_and_query_returns_relevant_chunk():
    vs = VectorStore()

    documents = [
        "AI is a subset of Computer Science.",
        "Bananas are a good source of potassium.",
    ]

    vs.build_index(documents)
    results = vs.query("Tell me about AI", top_k=1)

    assert len(results) == 1
    assert "AI" in results[0]
