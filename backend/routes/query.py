from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.llm.prompt import build_prompt


router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_system(request: Request, query_request: QueryRequest):
    rag = request.app.state.rag

    query = query_request.query

    # Retrieve context
    results = rag["hybrid"].retrieve(query)
    context = rag["hybrid"].format_context(results)

    # Build prompt
    prompt = build_prompt(query, context)

    # Generate response
    response = rag["llm"].generate(prompt)

    # Validate response
    validation = rag["validator"].validate(response)

    # Store interaction in memory
    rag["memory"].add(query, response)

    return {
        "query": query,
        "answer": response,
        "confidence": validation["confidence"],
        "invalid_claims": validation["invalid"],
    }
