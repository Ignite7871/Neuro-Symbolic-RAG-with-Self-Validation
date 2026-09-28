import re

class KGBuilder:
    def __init__(self):
        pass

    def clean_entity(self, text):
        # remove extra phrases
        text = re.sub(r"that .*", "", text)
        text = re.sub(r"using .*", "", text)
        return text.strip()

    def extract_triples(self, text):
        triples = []

        # subset_of (priority)
        pattern_subset = re.findall(r"(.+?) is a subset of (.+?)(?:\.|$)", text)
        for subj, obj in pattern_subset:
            obj = self.clean_entity(obj)
            triples.append((subj.strip(), "subset_of", obj))

        # used_in (split multiple domains)
        pattern_used = re.findall(r"(.+?) is used in (.+?)(?:\.|$)", text)
        for subj, objs in pattern_used:
            domains = objs.split(",")
            for d in domains:
                d = d.strip()

                # remove leading "and"
                d = re.sub(r"^and\s+", "", d)

                triples.append((subj.strip(), "used_in", d))

        # generic "is"
        pattern_is = re.findall(r"(.+?) is (.+?)(?:\.|$)", text)
        for subj, obj in pattern_is:

            # skip if already handled
            if "subset of" in obj or "used in" in obj:
                continue

            triples.append((subj.strip(), "is", obj.strip()))

        return triples