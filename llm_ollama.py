#IF USING THEN RENAME TO LLM.PY

import os
import requests
import json
import re

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

def clean_text(text):
    return re.sub(r"```json|```", "", text).strip()

def ollama_generate(prompt: str) -> str:
    """Send a prompt to Ollama and return the response text."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"]


def plan_tasks(user_input: str):
    prompt = f"""
Return ONLY valid JSON array. No explanation, no markdown, no extra text.
Each item must have this exact shape:
{{"tool": "...", "args": "..."}}
Available tools: nmap, gobuster, zap
User request:
{user_input}
"""
    try:
        text = ollama_generate(prompt)
        text = clean_text(text)
        return json.loads(text)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "raw": text}
    except requests.RequestException as e:
        return {"error": f"Ollama request failed: {e}"}
    except Exception as e:
        return {"error": str(e)}


# ===== SUMMARIZER =====
def summarize_results(nmap_output="", gobuster_output="", zap_alerts=None):
    prompt = f"""
You are a cybersecurity analyst. Summarize the following scan results concisely.

Nmap output:
{nmap_output}

Gobuster output:
{gobuster_output}

ZAP alerts:
{zap_alerts}

Provide exactly:
- Open ports summary
- Directories found
- Key vulnerabilities
- Risk level (Low / Medium / High)
- Top 3 recommendations
"""
    try:
        return ollama_generate(prompt)
    except requests.RequestException as e:
        return f"Ollama request failed: {e}"
    except Exception as e:
        return f"LLM Error: {e}"