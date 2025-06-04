from backend.WatchStatus import WatchStatus
def confidence_branch(state: WatchStatus):
    JudgmentGate = "automation" if state['confidence']['score'] >= 0.75 else "escalation"
    return JudgmentGate
