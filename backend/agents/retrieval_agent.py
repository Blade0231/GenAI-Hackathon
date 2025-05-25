from crewai import Agent
from crewai_tools import tool
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

@tool("retrieve_chunks")
class RetrievalTool:
    def __init__(self):
        with open("data/vector_store/faiss_index.pkl", "rb") as f:
            self.index, self.texts = pickle.load(f)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def run(self, query: str) -> str:
        query_vec = self.embedder.encode([query])
        D, I = self.index.search(query_vec, k=5)
        return "\n\n".join([self.texts[i] for i in I[0]])


retrieval_tool = RetrievalTool()

retrieval_agent = Agent(
    name="RetrievalAgent",
    role="Finds relevant PDF chunks",
    goal="Retrieve relevant context for a given query",
    backstory="Specialist in semantic search using FAISS",
    tools=[retrieval_tool],
    verbose=True
)
