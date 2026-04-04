import requests

class LLM:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]