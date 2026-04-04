import datetime

class EpisodicMemory:
    def __init__(self):
        self.memory = []

    def add(self, query, response):
        entry = {
            "query": query,
            "response": response,
            "timestamp": datetime.datetime.now()
        }
        self.memory.append(entry)

    def get_recent(self, k=3):
        return self.memory[-k:]

    def search(self, keyword):
        results = []

        for entry in self.memory:
            if any(word.lower() in entry["query"].lower() for word in keyword.split()):
                results.append(entry)

        return results