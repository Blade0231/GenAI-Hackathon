from typing import TypedDict, Optional

class WatchStatus(TypedDict):
    incident_raw_text: str
    incident_short_description: Optional[str]
    incident_description: Optional[str]
    incident_opened_date: Optional[str]
    knowledge: Optional[str]
    reasoning_result: Optional[str]
    root_cause: Optional[str]
    resolution_steps: Optional[str]
    confidence: Optional[str]
    pre_output: Optional[str]
    final_response: Optional[str]
 