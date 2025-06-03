class HumanEscalationAgent:
    def escalate(self, reasoning_text: str) -> str:
        # Build a Mail or Teams Message
        # We can get email DL from Incident Contact Field from Input Dataset
        return f"Escalated to human operator. Reasoning: {reasoning_text}"
    
    