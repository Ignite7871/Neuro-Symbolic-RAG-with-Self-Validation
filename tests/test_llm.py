import pytest

from backend.llm.model import LLM


def test_llm_generate_wraps_connection_errors():
    llm = LLM(url="http://localhost:1/unreachable")

    with pytest.raises(RuntimeError):
        llm.generate("hello")
