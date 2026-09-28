from backend.llm.prompt import build_prompt


def test_prompt_contains_query_and_context():
    query = "Where is AI used?"
    context = "AI is used in healthcare."

    prompt = build_prompt(query, context)

    assert query in prompt
    assert context in prompt
    assert "Context:" in prompt
    assert "Question:" in prompt
