from backend.WatchStatus import WatchStatus

def automation_node(state: WatchStatus,llm):
    joined_steps = "\n".join([f"- {step}" for step in state['resolution_steps']])

    prompt = f"""
        You are a DevOps automation assistant.

        The following are manual resolution steps identified by a Site Reliability Engineer:

        {joined_steps}

        Please generate an **Ansible playbook or task list** to automate these steps. 
        Use proper syntax and relevant modules. Output only the code.
        Ensure the playbook is idempotent and handles errors gracefully.

    """
    TowerForge = llm.send_message(prompt)
    # return {"pre_output": TowerForge.text}
    return {"pre_output": TowerForge}
