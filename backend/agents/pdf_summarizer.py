from crewai import Agent
from langchain.tools import Tool
from langchain_community.document_loaders import PyPDFLoader

# LLM Imports
# from langchain.chat_models import ChatOpenAI  
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# llm = ChatOpenAI(temperature=0.3)  # Replace this with Hugging Face

# template = PromptTemplate(
#     input_variables=["content"],
#     template="Please summarize the following PDF content:\n\n{content}"
# )

# summarize_chain = LLMChain(llm=llm, prompt=template)

def summarize_pdf(path: str) -> str:
    loader = PyPDFLoader(path)
    pages = loader.load()
    text = "\n".join([p.page_content for p in pages[:3]]) # Truncated Text
    
    #llm_response = summarize_chain.run({"content": text})
    
    return text

summarize_pdf_tool = Tool(
    name="summarize_pdf",
    func=summarize_pdf,
    description="Summarizes the content of a PDF file."
)

summary_agent = Agent(
    name="PDFSummarizer",
    role="Summarizes PDF documents",
    goal="Quickly extract and summarize text from PDF documents.",
    tools=[summarize_pdf_tool],
    backstory="Expert in quickly summarizing PDF files.",
    verbose=True
)
