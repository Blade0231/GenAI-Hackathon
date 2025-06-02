from langgraph.graph import StateGraph, END
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.reasoning_agent import ReasoningAgent
from backend.agents.confidence_check_agent import ResolutionConfidence
from backend.agents.ansible_agent import AnsibleAutomationAgent
from backend.agents.escalation_agent import HumanEscalationAgent
from agents.summarizer_agent import SummarizerAgent

class IncidentState:
    def __init__(self, incident_summary):
        self.incident_summary = incident_summary
        self.docs = None
        self.reasoning_result = None
        self.confidence = None
        self.next_output = None
        self.final_response = None

def retrieval_node(state: IncidentState):
    retriever = RetrievalAgent()
    state.docs = retriever.retrieve(state.incident_summary)
    return state

def reasoning_node(state: IncidentState):
    reasoner = ReasoningAgent()
    state.reasoning_result = reasoner.reason(state.docs, state.incident_summary)
    return state

def confidence_node(state: IncidentState):
    confidence_agent = ResolutionConfidence()
    state.confidence = confidence_agent.check(state.reasoning_result)
    return state

def automation_node(state: IncidentState):
    ansible_agent = AnsibleAutomationAgent()
    state.next_output = ansible_agent.generate(state.reasoning_result["response"])
    return state

def escalation_node(state: IncidentState):
    escalation_agent = HumanEscalationAgent()
    state.next_output = escalation_agent.escalate(state.reasoning_result["response"])
    return state

def summarization_node(state: IncidentState):
    summarizer = SummarizerAgent()
    state.final_response = summarizer.summarize(state.next_output)
    return state

def confidence_branch(state: IncidentState):
    return "automation" if state.confidence == "high" else "escalation"

# Build the LangGraph workflow
workflow = StateGraph(IncidentState)
workflow.add_node("retrieval", retrieval_node)
workflow.add_node("reasoning", reasoning_node)
workflow.add_node("confidence", confidence_node)
workflow.add_node("automation", automation_node)
workflow.add_node("escalation", escalation_node)
workflow.add_node("summarization", summarization_node)

workflow.add_edge("retrieval", "reasoning")
workflow.add_edge("reasoning", "confidence")
workflow.add_conditional_edges("confidence", confidence_branch, {
    "automation": "automation",
    "escalation": "escalation"
})
workflow.add_edge("automation", "summarization")
workflow.add_edge("escalation", "summarization")
workflow.add_edge("summarization", END)
workflow.set_entry_point("retrieval")

graph = workflow.compile()

if __name__ == "__main__":
    incident_summary = "Service outage in authentication layer for component XYZ."
    state = IncidentState(incident_summary)
    final_state = graph.invoke(state)
    
    print("\nFinal Summary:\n", final_state.final_response)