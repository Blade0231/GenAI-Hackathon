from crewai import Agent
from langchain.tools import tool
import pandas as pd

# LLM Imports
# from langchain.chat_models import ChatOpenAI  # or any LLM
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# llm = ChatOpenAI(temperature=0.3) 

# insight_template = PromptTemplate(
#     input_variables=["table"],
#     template="Analyze this table data and give a brief summary of insights:\n\n{table}"
# )
# table_chain = LLMChain(llm=llm, prompt=insight_template)


@tool(description="Analyze tabular CSV data and provide key insights.")
def extract_insights(file_path: str) -> str:
    df = pd.read_csv(file_path)
    summary = f"Columns: {df.columns.tolist()}\n"
    summary += f"Top Rows:\n{df.head(2).to_string()}\n"
    summary += f"Missing Values: {df.isnull().sum().sum()}\n"

    #lnm_response = table_chain.run({"table": df.head(10).to_string()})

    return summary


table_agent = Agent(
    name="ExcelAnalyzer",
    role="Analyzes tabular data for insights",
    goal="Extract key stats, data quality metrics, and trends from structured data.",
    tools=[extract_insights],
    backstory="Provides descriptive insights on tabular data.",
    verbose=True
)