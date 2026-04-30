import os
import requests
import json
import re

def clean_text(text):
    return re.sub(r"```json|```", "", text).strip()


# ===== PLANNER =====
def plan_tasks(user_input: str):
    api_key = os.environ.get("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""
Return ONLY valid JSON array.

Each item:
{{"tool": "...", "args": "..."}}

Tools: nmap, gobuster, zap

User request:
{user_input}
"""

    try:
        response = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

        data = response.json()

        if "error" in data:
            return {"error": data["error"]}

        if "candidates" not in data:
            return {"error": "No candidates", "raw": data}

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        text = clean_text(text)

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}


# ===== SUMMARIZER =====
def summarize_results(nmap_output="", gobuster_output="", zap_alerts=None):
    api_key = os.environ.get("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""
You are a cybersecurity analyst.

Summarize the following:

Nmap:
{nmap_output}

Gobuster:
{gobuster_output}

ZAP:
{zap_alerts}

Provide:
- Open ports summary
- Directories found
- Key vulnerabilities
- Risk level (Low/Medium/High)
- Top 3 recommendations

Keep it concise.
"""

    try:
        response = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

        data = response.json()

        if "error" in data:
            return f"LLM Error: {data['error']}"

        if "candidates" not in data:
            return f"Invalid response: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"LLM Error: {str(e)}"