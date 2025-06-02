from langchain.chat_models import ChatOpenAI

class ReasoningAgent:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key="YOUR_KEY_HERE")

    def reason(self, context_docs: list, incident_summary: str) -> dict:
        context = "\n".join([doc.page_content for doc in context_docs])
        prompt = f"""
            You are a highly experienced Site Reliability Engineer (SRE) investigating a production incident.

            ### Incident Summary:
            {incident_summary}

            ### Retrieved Knowledge Base Context:
            {context}

            Based on the above information:

            1. Perform a **Root Cause Analysis**
            2. Propose a detailed, **step-by-step Resolution Plan**
            3. Assess and report your **Confidence Score (0.0 to 1.0)** in the proposed resolution based on:
            - Match between incident summary and context
            - Completeness of root cause traceability
            - Clarity of resolution steps

            ### Response Format (in Markdown):

            ```markdown
            ## Root Cause
            [Write detailed analysis of the issue, indicating affected systems, triggers, and breakdowns.]

            ## Resolution Steps
            1. [First resolution step]
            2. [Second step, and so on...]

            ## Confidence Score
            Confidence: [0.0 to 1.0]  
            Reasoning: [Justify the confidence score briefly]
        """
        response = self.llm.predict(prompt)
        return response