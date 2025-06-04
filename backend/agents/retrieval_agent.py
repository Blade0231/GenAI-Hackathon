from backend.WatchStatus import WatchStatus

def retrieve_knowledge_node(state: WatchStatus, KnowledgeKeep):
    # retriever = RetrievalAgent()
    # state.knowledge = retriever.retrieve(state.incident_summary)
    # return state
    query = f'''
    The articles as closer as possible which mention how to fix issues similar to this 
    issue short description: {state['incident_short_description']} 
    and this 
    issue description {state['incident_description']}, 
    and as recent as possible to the date {state['incident_opened_date']}'''

    TowerBrief = KnowledgeKeep.query(query_texts=[query], n_results=10)
    [all_docs] = TowerBrief["documents"]
    q_text = "\n".join(doc for doc in all_docs)
    return {"knowledge": q_text}
