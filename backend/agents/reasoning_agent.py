from backend.WatchStatus import WatchStatus
import json

def reasoning_node(state: WatchStatus, llm):
    # reasoner = ReasoningAgent()
    # state.reasoning_result = reasoner.reason(state.knowledge, state.incident_summary)
    # return state
    prompt = f"""
            You are a highly experienced Site Reliability Engineer (SRE) investigating a production incident.

            ### Incident Summary:

            Opened Date:
            {state['incident_opened_date']}

            Short Description:
            {state['incident_short_description']}

            Description:
            {state['incident_description']}

            ### Retrieved Knowledge Base Context:
            {state['knowledge']}

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
    TowerMind = llm.send_message(prompt)
    cleaned = TowerMind.text.strip().replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    return {"reasoning_result": TowerMind.text,"root_cause":parsed["root_cause"],"resolution_steps":parsed["resolution_steps"],"confidence":parsed["confidence"]}
