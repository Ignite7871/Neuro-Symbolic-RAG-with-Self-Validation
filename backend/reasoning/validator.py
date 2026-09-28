import re

class Validator:
    def __init__(self, graph_store):
        self.graph_store = graph_store

    def extract_entities(self, text):
        words = re.findall(r'\b[A-Za-z]+\b', text)
        return [w.lower() for w in words]

    def validate(self, response):
        graph = self.graph_store.get_all()

        valid = []
        invalid = []

        response_entities = self.extract_entities(response)

        stop_words = {"ai", "is", "in", "and", "used", "the", "of"}

        # check valid facts
        for (subj, rel, obj) in graph:
            obj_lower = obj.lower()

            if obj_lower in response.lower() and len(obj_lower) > 2:
                valid.append(obj)

        # check invalid claims
        for word in response_entities:
            match = any(word in obj.lower() for (_, _, obj) in graph)

            if not match and word not in stop_words:
                invalid.append(word)

        # remove duplicates
        valid = list(set(valid))
        invalid = list(set(invalid))

        # confidence score
        total = len(valid) + len(invalid)
        confidence = len(valid) / total if total > 0 else 0

        return {
            "valid": valid,
            "invalid": invalid,
            "confidence": round(confidence, 2)
        }