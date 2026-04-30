
# Kali: Agentic Cyber-Defense

**Girish Mundra**



## 1. Project Overview

This project builds an **autonomous AI interface for Kali Linux** that converts natural language security requests into executable security operations inside Dockerized environments.

It uses an LLM-driven pipeline for cybersecurity automation:

> Natural Language → LLM Planner → Tool Execution → LLM Analysis → Final Report

### Core Components

* Dockerized Kali Linux environment
* Nmap (network scanning)
* Gobuster (directory enumeration)
* OWASP ZAP (web vulnerability scanning)
* Ollama (local) / Gemini LLM (planning + analysis)
* FastAPI backend



## 2. Infrastructure Setup

### Server Environment

* Remote GPU server accessed via SSH
* Docker runtime on host

### Containers

**Kali Linux Container**

* Name: `girish-container`
* Tools: nmap, gobuster, security utilities

**OWASP ZAP Container**

* Name: `zap-container`
* Image: `ghcr.io/zaproxy/zaproxy:stable`
* Port: 8080
* Used for spider-based vulnerability scanning

**Ollama Container (LLM Fallback/Optional)**

* Container name: \texttt{ollama-container}
* Runs Ollama framework for local LLM inference
* Model used: Llama3 (CPU-based fallback)
* Note: GPU acceleration was not available due to missing CUDA support inside container

## 3. Backend Architecture

Built using **FastAPI**, structured into modules:

* `main.py` → API orchestration
* `llm.py` → LLM planner + summarizer
* `executor.py` → Docker command execution
* `validator.py` → security validation layer
* `zap.py` → OWASP ZAP integration



## 4. System Workflow

### Step 1: User Input

Example:

```text
scan directory vulnerability scanme.nmap.org
```



### Step 2: LLM Planner

LLM converts input into structured execution plan:

```json
[
  { "tool": "nmap", "args": "nmap -F scanme.nmap.org" },
  { "tool": "gobuster", "args": "gobuster dir -u http://scanme.nmap.org ..." },
  { "tool": "zap", "args": "scanme.nmap.org" }
]
```



### Step 3: Validation Layer

* Allowed tools: nmap, gobuster, zap
* Blocks unsafe commands (rm, shutdown, pipes, etc.)
* Enforces valid JSON schema



### Step 4: Tool Execution

Commands run inside Docker:

```python
container.exec_run(command)
```

**ZAP scanning:**

* Spider crawling
* Medium & high severity vulnerabilities
* Deduplicated alerts



### Step 5: LLM Analysis

Gemini/Ollama summarizes outputs:

* Open ports (Nmap)
* Directory findings (Gobuster)
* Vulnerabilities (ZAP)
* Risk assessment
* Actionable recommendations



## 5. API Response Format

```json
{
  "plan": [...],
  "results": {
    "nmap": "...",
    "gobuster": "...",
    "zap": [...]
  },
  "summary": "..."
}
```



## 6. Key Design Decisions

* LLM used only for planning + analysis (not execution)
* Fully isolated Docker-based execution
* Structured JSON replaces keyword parsing
* Modular FastAPI architecture
* Easily extensible tool system



## 7. Environment Setup

Run backend:

```bash
GEMINI_API_KEY="your_api_key_here" uvicorn app.main:app --host 0.0.0.0 --port 5050
```

Example:

```bash
GEMINI_API_KEY="my_api_key" uvicorn app.main:app --host 0.0.0.0 --port 5050
```



## 8. Future Improvements

### 1. Multi-Step Adaptive Agent

Auto-chain tools based on findings (e.g., open HTTP → trigger Gobuster/ZAP)

### 2. Robust JSON Parsing

Stricter handling of malformed LLM outputs

### 3. Retry / Fallback Models

Use Ollama or alternative LLMs during API failures

### 4. Structured Tool Arguments

Replace raw strings with typed argument schemas

### 5. Report Generation

Generate full PDF/HTML penetration testing reports

### 6. Attack Flow Visualization

Graph-based representation of scan-to-exploitation flow



## 9. Conclusion

This system demonstrates an **LLM-driven autonomous cybersecurity pipeline** combining:

* Natural language understanding
* Containerized deterministic execution
* Structured validation
* AI-based security analysis

It forms a foundation for **autonomous penetration testing agents** and future adaptive security systems.
