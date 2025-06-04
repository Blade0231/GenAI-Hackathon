from backend.WatchStatus import WatchStatus

def summarization_node(state: WatchStatus,llm):
    prompt = f"""
        You are a technical incident response assistant summarizing the resolution of a production incident for stakeholders.

        ### Incident Short Description:
        {state['incident_short_description']}

        ### Incident Description:
        {state['incident_description']}
        
        ### Incident Summary:

        Opened Date:
        {state['incident_opened_date']}

        Short Description:
        {state['incident_short_description']}

        Description:
        {state['incident_description']}

        ### Context Used:
        {state['knowledge']}

        ### Root Cause (From Reasoning Agent):
        {state['root_cause']}

        ### Resolution (From Reasoning Agent):
        {state['resolution_steps']}

        ### Confidence Score:
        {state['confidence']}

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
        {state['confidence']['score']}  
        [Brief reason why the confidence score was high/low.]

        ## ✅ Final Notes
        [Call out any follow-up actions, human approvals, or automation triggers.]
        Be precise, avoid fluff, and keep it under 200 words.
    """
    WatchNarrator = llm.send_message(prompt)
    return {"final_response": WatchNarrator.text}
