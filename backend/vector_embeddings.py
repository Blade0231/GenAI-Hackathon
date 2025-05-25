
import os
import pickle
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

def preprocess_pdf(pdf_path:str=None, save_path:str=None):
    reader = PdfReader(pdf_path)
    chunks = [page.extract_text() for page in reader.pages if page.extract_text()]
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = embedder.encode(chunks)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        pickle.dump((index, chunks), f)


if __name__=="__main__":
    preprocess_pdf(pdf_path="data/10q_form.pdf", save_path="data/vector_store/faiss_index.pkl")