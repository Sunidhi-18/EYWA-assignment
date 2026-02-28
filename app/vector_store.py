from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []

    def build_index(self, chunks):
        """
        Create FAISS index from transcript chunks
        """
        self.text_chunks = chunks

        embeddings = self.model.encode(chunks)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def search(self, query, top_k=3):
        """
        Retrieve most relevant chunks
        """
        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        results = [self.text_chunks[i] for i in indices[0]]

        return " ".join(results)