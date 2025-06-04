from backend.WatchStatus import WatchStatus
from backend.WatchTower import build_watch_tower
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from google.api_core.exceptions import ResourceExhausted

def langgraph(incident_raw_text: str) -> str:
    state = WatchStatus(incident_raw_text)
    graph = build_watch_tower()
    final_state = graph.invoke(state)
    return final_state['final_response']

def html_to_clean_text(html: str, max_length: int = 1000000) -> str:
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style
    for tag in soup(["script", "style", "footer", "nav"]):
        tag.decompose()

    # Get text
    text = soup.get_text(separator="\n")

    # Remove excessive whitespace
    text = re.sub(r'\n+', '\n', text)  # collapse newlines
    text = re.sub(r'[ \t]+', ' ', text)  # collapse spaces


    # Truncate to avoid token overload
    return text.strip()[:max_length]

def get_article_cleaning_prompt(text_clean) -> str:
    
    prompt = f"""
        You are an IT Service Management (ITSM) assistant. I will provide you with the **raw text or HTML content of a technical Knowledge Article**. Based **strictly and only on the content provided**, extract structured and meaningful information that will later be used to recommend resolution steps for IT incidents.

        Your goal is to make this knowledge article machine-usable for incident triage, resolution recommendation, and automation.

        📄 **Tasks (DO NOT infer or hallucinate — only use what's present):**

        ---

        1. **Title and Metadata**  
        - Extract the article **title** (or derive a concise title from the content)  
        - Extract the **publication date** or **last updated date** (if available)  
        - Identify **affected system(s)** or **components** (e.g., Windows Server, MySQL, Jenkins)  
        - Identify the **issue type** (e.g., service not starting, login failure, high CPU usage)  

        2. **Problem Signature**  
        Extract the symptoms, error messages, or problem patterns described.  
        Return as a list:
        - Specific error codes (e.g., `0x80070005`)
        - Log messages (e.g., "Connection refused")
        - Behavioral symptoms (e.g., "Server hangs after restart")

        3. **Root Cause (if present)**  
        Extract any explicitly mentioned causes or explanations for the issue.  
        This could include misconfigurations, resource limits, expired certificates, etc.

        4. **Step-by-Step Resolution**  
        List all **concrete troubleshooting or resolution steps** in clear, actionable format.  
        Use bullet points or numbered steps. Include any:
        - Commands
        - Configuration changes
        - System restarts
        - Diagnostic steps
        - Log file paths
        - Screenshots referenced (ignore image content)

        5. **Automation Opportunities**  
        Highlight any step that **could be automated** using tools like Ansible or shell scripts.  
        Provide:
        - Command-line equivalent if shown
        - Shell or YAML syntax (if included)
        - Brief summary of the task (e.g., "Restart nginx and clear logs")

        6. **Precautions or Warnings**  
        Extract any safety notices or cautions (e.g., "Back up config before restarting", "May impact production users").

        7. **Related Topics or Tags**  
        Tag the article with relevant **topics or tags** that describe its content.  
        Examples: `linux`, `apache`, `networking`, `SSL`, `ansible`, `disk usage`, `SQL Server`

        ---

        ⚠️ Do not assume any information not present in the article.  
        ⚠️ Return content in **Markdown** with bold section headers and clean formatting.  
        ⚠️ Do NOT return JSON or use code blocks.

        ---

        📥 **Input Format**:
        You will be given the article in plain text or HTML format.

        --- BEGIN ARTICLE CONTENT ---
        {text_clean}
        --- END ARTICLE CONTENT ---
        """

    return prompt

# def get_article_summary(client, raw_text: str, max_length: int = 1000000):
#     print('🔍 Cleaning HTML and generating summarization prompt...')
#     text_cleaned = html_to_clean_text(raw_text, max_length)
#     prompt = get_article_cleaning_prompt(text_cleaned)

#     print('🤖 Getting model response...')
#     response = client.models.generate_content(
#         model="gemini-2.0-flash-001", contents=prompt
#     )
#     model_output = response.text.strip()
#     return model_output

def get_article_summary(llm, raw_text: str, max_length: int = 1000000):
    print('🔍 Cleaning HTML and generating summarization prompt...')
    text_cleaned = html_to_clean_text(raw_text, max_length)
    prompt = get_article_cleaning_prompt(text_cleaned)

    print('🤖 Getting model response...')
    summary = llm.send_message(prompt)
    return summary

def get_article_summary_with_retry(client, raw_text, max_length=1000000):
    try:
        return get_article_summary(client, raw_text, max_length=max_length)
    except ResourceExhausted as e:
        print("⚠️ Quota limit hit. Trying with smaller input...")
        if max_length > 50000:
            time.sleep(10)
            return get_article_summary_with_retry(client, raw_text, max_length=max_length // 1.5)
        else:
            print("❌ Input is too small. Giving up.")
            return None

    except Exception as e:
        # Check if it's a quota error that wasn't caught properly
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            print("⚠️ Quota limit hit (generic handler). Trying with smaller input...")
            if max_length > 50000:
                time.sleep(10)
                return get_article_summary_with_retry(client, raw_text, max_length=max_length // 1.5)
            else:
                print("❌ Input is too small. Giving up.")
                return None

        print(f"❌ Failed due to error: {e}")
        return None

def dump_article_summaries(TowerArchives, client):
    kb_df = pd.read_excel("data/raw/MOCKDATA.xlsx")
    kb_df = kb_df[['KB Number','KB Title', 'KB Steps', 'Ansible Automatable', 'Category']]

    summaries = []

    if TowerArchives.count() < 30:
        # Loop through each Knowledge Article
        for index, row in kb_df.iterrows():
            print(f"Processing: {row['KB Title']}")
            
            try:
                summary_text = get_article_summary_with_retry(client, raw_text=f"Title: {row['KB Title']} \nResolutionSteps:\n{row['KB Steps']} \nAnsible Automatable: {row['Ansible Automatable']} \nCategory: {row['Category']}")
                
                if summary_text:
                    summaries.append({
                        "Number": row['KB Number'],
                        "Summary": summary_text
                    })
    
            except Exception as e:
                print(f"❌ Failed to summarize {row['KB Number']}: {e}")
            
        
        print(f"✅ Finished processing {len(summaries)} Articles.")

    else:
        print("Information already available")

    documents = [data["Summary"] for  data in summaries]
    metadata = [
        {k: v for k, v in data.items() if k != "Summary"}
        for data in summaries
    ]

    TowerArchives.add(documents=documents, ids = [str(j) for j in range(len(documents))],metadatas = metadata)
