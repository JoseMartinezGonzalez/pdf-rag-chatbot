from app.services.embeddings import EmbeddingsManager

class Retriever:
    def __init__(self):
        self.em = EmbeddingsManager()

    def retrieve(self, question: str, top_k: int = 4):
        docs = self.em.search(question, top_k=top_k)
        return docs
