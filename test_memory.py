from backend.memory.episodic import EpisodicMemory

memory = EpisodicMemory()

# Simulate interactions
memory.add("What is AI?", "AI is artificial intelligence")
memory.add("Where is AI used?", "AI is used in healthcare, finance, robotics")

# Get recent
print("\nRecent Memory:")
for m in memory.get_recent():
    print(m)

# Search memory
print("\nSearch Memory (AI):")
results = memory.search("AI")

for r in results:
    print(r)