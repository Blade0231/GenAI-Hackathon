from langchain.chat_models import ChatOpenAI

class SummarizerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key="YOUR_KEY_HERE")

    def reason(self, state):
        prompt = f"""
            You are a technical incident response assistant summarizing the resolution of a production incident for stakeholders.

            ### Incident Summary:
            {state.incident_summary}

            ### Context Used:
            {state.docs}

            ### Root Cause and Resolution (From Reasoning Agent):
            {state.reasoning_result}

            ### Confidence Score:
            {state.confidence}

            Please produce a **concise summary** in markdown with the following structure:

            ```markdown
            ## 📝 Incident Recap
            [A short paragraph restating the incident in simple terms.]

            ## 🧠 Root Cause Summary
            [A 2-3 sentence summary of the root cause.]

            ## 🔧 Key Resolution Steps
            - [Step 1]
            - [Step 2]
            - ...

            ## 📊 Confidence Score
            {state.confidence}  
            [Brief reason why the confidence score was high/low.]

            ## ✅ Final Notes
            [Call out any follow-up actions, human approvals, or automation triggers.]
            Be precise, avoid fluff, and keep it under 200 words.
        """
        response = self.llm.predict(prompt)
        return response