import json
from backend.WatchStatus import WatchStatus
def parse_raw_incident(state: WatchStatus, llm) -> WatchStatus:
    incident_extraction_prompt = f"""
    Extract the following structured information from the raw incident text:
    1. Incident Opened Date (must be in YYYY-MM-DD format) - Date when the incident was opened
    2. Incident Short Description - Short description of the incident in max 10-12 words
    3. Incident Description - Detailed description of the incident in max 100 words

    User prompt:
    {state["incident_raw_text"]}

    Respond ONLY in raw JSON, without any explanation or markdown . Format:
    
    {{
      "incident_opened_date": "YYYY-MM-DD",
      "incident_short_description": "",
      "incident_description": ""
    }}
    """
    response = llm.send_message(incident_extraction_prompt)

    InputMason = response.text.strip().replace("```json", "").replace("```", "").strip()
    parsed = json.loads(InputMason)

    return {"incident_opened_date": parsed["incident_opened_date"], "incident_short_description": parsed["incident_short_description"], "incident_description": parsed["incident_description"]}
