class VectorStore:
    def __init__(self):
        self.memory = []

    def store(self, record):
        print(f"[VectorStore] Memorizing output: {record}")
        self.memory.append(record)

    def get_all(self):
        return self.memory
