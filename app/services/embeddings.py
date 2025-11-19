import os
import pickle
import numpy as np
import faiss
import openai
from typing import List

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")
openai.api_key = OPENAI_KEY

EMBED_MODEL = "text-embedding-3-small"  # or text-embedding-3-large
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../vector_store/index.faiss")
META_PATH = os.path.join(os.path.dirname(__file__), "../vector_store/meta.pkl")

class EmbeddingsManager:
    def __init__(self):
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        self.dim = 1536  # change if model different; adjust if using different model
        self.index = None
        self.meta = []  # list of dicts {id, source, text}
        self._load()

    def _load(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)
                with open(META_PATH, "rb") as f:
                    self.meta = pickle.load(f)
                self.dim = self.index.d
            except Exception:
                self.index = None
                self.meta = []
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def _embed(self, texts: List[str]) -> List[List[float]]:
        resp = openai.Embedding.create(model=EMBED_MODEL, input=texts)
        return [r["embedding"] for r in resp["data"]]

    def add_documents(self, texts: List[str], source: str = "upload"):
        batch_size = 16
        ids = list(range(len(self.meta), len(self.meta) + len(texts)))
        # compute embeddings in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            embs = self._embed(batch)
            arr = np.array(embs).astype('float32')
            self.index.add(arr)
        # extend meta
        for idx, t in zip(ids, texts):
            self.meta.append({"id": idx, "source": source, "text": t})
        self._save()

    def _save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.meta, f)

    def search(self, query: str, top_k: int = 4):
        q_emb = self._embed([query])[0]
        v = np.array([q_emb]).astype('float32')
        D, I = self.index.search(v, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.meta):
                results.append(self.meta[idx])
        return results
