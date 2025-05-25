from crewai import Agent
from crewai_tools import tool
from transformers import pipeline

@tool("generate_answer")
class ReasoningTool:
    def __init__(self):
        self.generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device=0)

    def run(self, context_and_query: str) -> str:
        prompt = f"Answer the following based on the context:\n{context_and_query}"
        result = self.generator(prompt, max_length=512, do_sample=True)
        return result[0]['generated_text']

reasoning_tool = ReasoningTool()

reasoning_agent = Agent(
    name="ReasoningAgent",
    role="Analyzes query and context",
    goal="Use retrieved chunks to answer the query accurately",
    backstory="Expert in analyzing and answering complex queries",
    tools=[reasoning_tool],
    verbose=True
)
