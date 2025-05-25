from crewai import Agent
from crewai_tools import tool
from transformers import pipeline

@tool("summarize_text")
class SummarizationTool:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def run(self, text: str) -> str:
        return self.summarizer(text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]

summarization_tool = SummarizationTool()

summarizer_agent = Agent(
    name="SummarizerAgent",
    role="Summarizes documents and answers",
    goal="Generate concise summaries of documents and outputs",
    backstory="Efficient summarizer for LLM outputs and large text blocks",
    tools=[summarization_tool],
    verbose=True
)
