from backend.utils import dump_article_summaries
from backend.WatchTower import build_watch_tower
from backend import DB_NAME
import chromadb
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from backend import GOOGLE_API_KEY
from google.genai import types
from google.api_core import retry

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        response = google_client.models.embed_content(
            model="models/text-embedding-004",
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task,
            ),
        )
        return [e.values for e in response.embeddings]
    
# client is the gemini client
google_client = genai.Client(api_key=GOOGLE_API_KEY)

# llm is the gemini model
llm = google_client.chats.create(model="gemini-2.0-flash-001")

chroma_client = chromadb.Client(Settings(
    is_persistent=True,
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))

# embed_fn is the gemini embedding function
embed_fn = GeminiEmbeddingFunction(google_client)

# set the document mode to true
embed_fn.document_mode = True

# TowerArchives is the croma db
TowerArchives = chroma_client.get_or_create_collection(
    name=DB_NAME, embedding_function=embed_fn
)

# Dump the article summaries to the database
# dump_article_summaries(TowerArchives,google_client)

# Build the watch tower graph
TowerGraph = build_watch_tower(llm, TowerArchives)

def run_watch_tower(initial_state, graph=TowerGraph):
    output_state = graph.invoke(initial_state)
    return output_state["final_response"]    

if __name__ == "__main__":
    
    raw_issue = "My USB flash drive is physically damaged, and I need assistance in recovering critical files from it."
    initial_state = {"incident_raw_text":raw_issue}

    output_state = run_watch_tower(graph=TowerGraph, initial_state=initial_state)
    print("\nOutput:\n", output_state['final_response']) 