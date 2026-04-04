class GraphStore:
    def __init__(self):
        self.graph = []

    def add_triples(self, triples):
        for triple in triples:
            self.graph.append(triple)

    def get_all(self):
        return self.graph

    def query(self, entity):
        results = []

        for (subj, rel, obj) in self.graph:
            if entity.lower() in subj.lower() or entity.lower() in obj.lower():
                results.append((subj, rel, obj))

        return results