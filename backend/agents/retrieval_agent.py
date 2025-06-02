import pickle
import faiss
import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer

from backend import vector_db, embedding_model_path

class RetrievalAgent:
    def __init__(self):
        with open(f"{vector_db}/chunk_texts.pkl", "rb") as f:
            self.chunk_texts = pickle.load(f)

        self.index = faiss.read_index(f"{vector_db}/faiss.index")

        # === Load Embedding Tokenizer & Model (Local) ===
        self.embed_tokenizer = AutoTokenizer.from_pretrained(embedding_model_path)
        self.embed_model = AutoModel.from_pretrained(embedding_model_path)

    def retrieve(self, query: str = None, top_k: int = 5):
        inputs = self.embed_tokenizer(query, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = self.embed_model(**inputs)
        query_embedding = output.last_hidden_state.mean(dim=1).numpy()

        # Normalize query embedding
        query_embedding /= np.linalg.norm(query_embedding, axis=1, keepdims=True)

        # Search in index
        distances, indices = self.index.search(query_embedding, top_k)

        # Get matched text chunks
        results = [self.chunk_texts[i] for i in indices[0]]
        return results
    
