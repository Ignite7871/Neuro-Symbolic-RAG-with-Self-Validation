def build_prompt(query, context):
    prompt = f"""
You are an intelligent AI system.

Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer clearly and concisely.
"""

    return prompt