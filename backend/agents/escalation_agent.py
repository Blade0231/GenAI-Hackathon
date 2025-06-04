from backend.WatchStatus import WatchStatus
def escalation_node(state: WatchStatus):
    EscalationWarden = f"Escalated to human operator. Reasoning: {state['reasoning_result']}"
    return {"pre_output":EscalationWarden}