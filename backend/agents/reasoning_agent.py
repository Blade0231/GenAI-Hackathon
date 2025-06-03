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

            ### Response Format (JSON):

            ```json
            {{
            "root_cause": "A detailed explanation of what caused the incident, including affected components, triggers, and how the failure propagated.",
            "resolution_steps": [
                "Step 1: Describe the first fix or action taken.",
                "Step 2: Add more steps as needed.",
                "... etc."
            ],
            "confidence": {{
                "score": 0.0,
                "reasoning": "Explain why you assigned this confidence score (e.g., based on context match, prior similar incidents, ambiguity in data, etc.)."
            }}
            }}
            ```
            
            Only return the JSON object. Do not include any explanation or markdown formatting outside of the JSON.
        """
        response = self.llm.predict(prompt)
        return response