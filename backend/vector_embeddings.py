import numpy as np
import faiss
import pickle

from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, pipeline
import torch
import os
from pathlib import Path

from backend import llm_model_path, embedding_model_path, vector_db, text_file

def pull_and_save_models():
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
    model = AutoModel.from_pretrained(embedding_model_name)

    tokenizer.save_pretrained(embedding_model_path)
    model.save_pretrained(embedding_model_path)

    llm_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
    model = AutoModelForCausalLM.from_pretrained(llm_model_name)

    tokenizer.save_pretrained(llm_model_path)
    model.save_pretrained(llm_model_path)    


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def embed(texts, tokenizer, model):
    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()

# Normalize embeddings (Cosine similarity ≈ L2 norm of normalized vectors)
def normalize(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms


def create_vector_db():
    raw_text = Path(text_file).read_text()
    text_chunks = chunk_text(text=raw_text, chunk_size=50, overlap=15)

    embeddings = embed(text_chunks)
    print("✅ Embedding shape:", embeddings.shape)

    normalized_embeddings = normalize(embeddings)

    # FAISS index for cosine similarity (using L2 on normalized vectors)
    embedding_dim = normalized_embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(normalized_embeddings)

    faiss.write_index(index, os.path.join(vector_db, "faiss.index"))

    # Save chunk metadata (to map results back to text)
    with open(os.path.join(vector_db, "chunk_texts.pkl"), "wb") as f:
        pickle.dump(text_chunks, f)

    print("✅ Embeddings stored and FAISS index saved.")


if __name__ == "__main__":
    create_vector_db()