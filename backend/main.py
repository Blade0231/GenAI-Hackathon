from crewai import Crew
from backend.agents.retrieval_agent import retrieval_agent
from backend.agents.reasoning_agent import reasoning_agent
from backend.agents.summarizer_agent import summarizer_agent

def run_rag_assistant(query: str):
    crew = Crew(
        agents=[retrieval_agent, reasoning_agent, summarizer_agent],
        tasks=[
            {
                "agent": retrieval_agent,
                "description": f"Retrieve relevant content for: {query}"
            },
            {
                "agent": reasoning_agent,
                "description": f"Generate a detailed answer using retrieved content and query: {query}"
            },
            {
                "agent": summarizer_agent,
                "description": f"Summarize the final output and full PDF"
            }
        ]
    )
    return crew.kickoff()

if __name__ == "__main__":
    print(run_rag_assistant("What are the key insights from this document?"))
