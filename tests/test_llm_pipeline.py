import pytest

from backend.reasoning.validator import Validator
from backend.retrieval.graph_store import GraphStore
from backend.llm.model import LLM


def _build_graph():
    graph = GraphStore()
    graph.add_triples([
        ("AI", "used_in", "healthcare"),
        ("AI", "used_in", "finance"),
        ("AI", "used_in", "robotics"),
    ])
    return graph


def test_validator_confidence_is_between_zero_and_one():
    validator = Validator(_build_graph())

    result = validator.validate("AI is used in healthcare and finance")

    assert 0 <= result["confidence"] <= 1
    assert "healthcare" in result["valid"]
    assert "finance" in result["valid"]


def test_validator_flags_unsupported_claims():
    validator = Validator(_build_graph())

    result = validator.validate("AI is used in agriculture")

    assert "agriculture" in result["invalid"]


def test_llm_generate_wraps_connection_errors():
    llm = LLM(url="http://localhost:1/unreachable")

    with pytest.raises(RuntimeError):
        llm.generate("hello")
