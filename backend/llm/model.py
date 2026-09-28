import requests

from backend.config import OLLAMA_URL, OLLAMA_MODEL

class LLM:
    def __init__(self, url=OLLAMA_URL, model=OLLAMA_MODEL):
        self.url = url
        self.model = model

    def generate(self, prompt):
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Could not reach Ollama at {self.url} (model='{self.model}'): {e}"
            ) from e

        return response.json()["response"]