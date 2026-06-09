# AI Usage Note

## Project: AI Docker Natural Language Health Dashboard

**Version:** 1.0.0
**Status:** ✅ Production Ready
**Last Updated:** 2026-06-08

---

## Overview

This project is a full-stack AI-powered Docker management dashboard that allows users to control Docker containers using natural language commands. It uses Ollama (llama3) for LLM translation, a ReAct-style agent loop with 7 visible steps, Streamlit for the UI, SQLite for logging, and GitHub API for external integration.

---

## Document Index

| Document | Description |
|----------|-------------|
| [Sample_Data.md](./Sample_Data.md) | Sample container data, database records, and expected dashboard output |
| [Test_Cases.md](./Test_Cases.md) | Test commands, expected results, and demo script reference |
| [Supporting_Documents.md](./Supporting_Documents.md) | Project statistics, tech stack, architecture, and deployment guides |

---

## How AI Is Used

### 1. Natural Language to Docker Command Translation
User types plain English (e.g., `restart nginx`) → Ollama llama3 translates to a structured JSON action → Docker SDK executes the operation.

### 2. ReAct Agent Loop (7 Steps)
Every command runs through a visible reasoning loop:

| Step | Name | Description |
|------|------|-------------|
| 1 | User Request | Accept and parse the natural language input |
| 2 | AI Analysis | Ollama translates the input to a JSON action |
| 3 | Tool Selection | Determine which Docker operation to run |
| 4 | Tool Execution | Execute via Docker SDK |
| 5 | Result Collection | Gather raw output |
| 6 | Summary Generation | Create a human-readable response |
| 7 | Response Return | Display result to user |

### 3. Prompt Logging
All AI interactions are logged to:
- **SQLite database** — `data/dashboard.db` → `prompt_logs` table
- **Text file** — `logs/prompt_log.txt`

Each log entry includes: timestamp, user prompt, generated action, execution result, and execution time in ms.

---

## Quick Start

```bash
# Docker Compose (recommended)
docker-compose up -d
docker exec -it ollama-service ollama pull llama3
# Open: http://localhost:8501

# Local Python
pip install -r requirements.txt
ollama serve && ollama pull llama3
streamlit run app.py
```

---

## Key Files

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 442 | Main Streamlit app — 7 pages |
| `agent.py` | 234 | ReAct agent loop |
| `docker_manager.py` | 272 | Docker SDK wrapper |
| `llm.py` | 263 | Ollama LLM integration |
| `database.py` | 213 | SQLite management |
| `github_api.py` | 105 | GitHub API integration |

---

*See linked documents for sample data, test cases, and full technical details.*
