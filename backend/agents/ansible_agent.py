import re
from langchain.chat_models import ChatOpenAI

class AnsibleAutomationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key="YOUR_KEY_HERE")

    def extract_resolution_steps(self, markdown_response: str) -> list:
        """
        Extracts the resolution steps from the markdown block.
        Assumes steps are in a numbered list under '## Resolution Steps'
        """
        steps_section = re.search(r'## Resolution Steps(.*?)##', markdown_response, re.DOTALL)
        if not steps_section:
            steps_section = re.search(r'## Resolution Steps(.*)', markdown_response, re.DOTALL)

        if not steps_section:
            return []

        steps_block = steps_section.group(1).strip()
        steps = re.findall(r'\d+\.\s+(.*)', steps_block)
        return steps

    def generate(self, reasoning_text: str) -> str:
        resolution_steps = self.extract_resolution_steps(reasoning_text)
        
        joined_steps = "\n".join([f"- {step}" for step in resolution_steps])

        prompt = f"""
            You are a DevOps automation assistant.

            The following are manual resolution steps identified by a Site Reliability Engineer:

            {joined_steps}

            Please generate an **Ansible playbook or task list** to automate these steps. 
            Use proper syntax and relevant modules. Output only the code.
            Ensure the playbook is idempotent and handles errors gracefully.

        """
        response = self.llm.predict(prompt)
        return response