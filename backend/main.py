from backend.utils import dump_article_summaries
from backend.WatchTower import build_watch_tower
from backend import DB_NAME, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION, OPENAI_API_KEY
import chromadb
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import AzureOpenAI

# client is the azure client
openai_client = AzureOpenAI(
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
)

class ChatLLM:
    def __init__(self, client, deployment_name, system_prompt="You are a helpful assistant."):
        self.client = client
        self.deploymet_name = deployment_name
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def send_message(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.deploymet_name,
            messages=self.messages
        )

        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

    def reset(self, system_prompt: str = None):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

# llm is the openAI model
llm = ChatLLM(openai_client, deployment_name="gpt-4o-7")

class AzureEmbeddingFunction(EmbeddingFunction):
    def __init__(self, client: AzureOpenAI):
        self.client = client
        self.document_mode = True

    def __call__(self, input: Documents) -> Embeddings:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=input
        )
        return [record.embedding for record in response.data]
    
chroma_client = chromadb.Client(Settings(
    is_persistent=True,
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))

embed_fn = AzureEmbeddingFunction(openai_client)
embed_fn.document_mode = True

# TowerArchives is the croma db
TowerArchives = chroma_client.get_or_create_collection(
    name=DB_NAME, embedding_function=embed_fn
)

# Dump the article summaries to the database
# dump_article_summaries(TowerArchives,llm)

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