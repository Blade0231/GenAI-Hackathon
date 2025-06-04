from backend.WatchStatus import WatchStatus
from backend.agents.parser import parse_raw_incident
from backend.agents.retrieval_agent import retrieve_knowledge_node
from backend.agents.reasoning_agent import reasoning_node
from backend.agents.ansible_agent import automation_node
from backend.agents.escalation_agent import escalation_node
from backend.agents.confidence_check_agent import confidence_branch
from backend.agents.summarizer_agent import summarization_node
from langgraph.graph import StateGraph, END

def build_watch_tower(llm, knowledge_db):
    TowerFlow = StateGraph(WatchStatus)
    TowerFlow.add_node("parser", lambda state: parse_raw_incident(state, llm))
    TowerFlow.add_node("retrieval", lambda state: retrieve_knowledge_node(state, knowledge_db))
    TowerFlow.add_node("reasoning", lambda state: reasoning_node(state, llm))

    TowerFlow.add_node("automation", lambda state: automation_node(state, llm))
    TowerFlow.add_node("escalation", escalation_node)
    TowerFlow.add_node("summarization", lambda state: summarization_node(state, llm))

    TowerFlow.add_edge("parser", "retrieval")
    TowerFlow.add_edge("retrieval", "reasoning")

    TowerFlow.add_conditional_edges("reasoning", confidence_branch, {
        "automation": "automation",
        "escalation": "escalation"
    })
    TowerFlow.add_edge("automation", "summarization")
    TowerFlow.add_edge("escalation", "summarization")
    TowerFlow.add_edge("summarization", END)
    
    TowerFlow.set_entry_point("parser")

    return TowerFlow.compile()
