<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=26&pause=1000&color=6C63FF&center=true&vCenter=true&width=760&lines=5-Day+AI+Agents+%26+Frameworks+Internship;TNSDC+%C3%97+IBM+%7C+Adroit+Technologies;Local+LLMs+%C2%B7+LangChain+%C2%B7+LangGraph+%C2%B7+MCP" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-6C63FF?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-6C63FF?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-0.2-6C63FF?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-6C63FF?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-6C63FF?style=for-the-badge)

**Hands-on work from the TNSDC IBM internship, delivered by Adroit Technologies.**
Five days, zero paid APIs: every agent here runs on a local model through Ollama.

</div>

---

## About

This repository holds all the code I wrote during a 5-day internship on building AI agents, run under the **Tamil Nadu Skill Development Corporation (TNSDC)** with **IBM**, and delivered by **Adroit Technologies**.

The internship went from the basics (one prompt to one local model) to a multi-agent system with persistent memory and a real Model Context Protocol (MCP) server. Everything runs offline on small open models (`tinyllama`, `qwen2.5:3b`), so no API keys are needed.

| | |
|---|---|
| 🏢 **Delivered by** | Adroit Technologies |
| 🤝 **Programme** | TNSDC × IBM |
| ⏱️ **Duration** | 5 days |
| 🧠 **Models** | `tinyllama`, `qwen2.5:3b` via Ollama |
| 👩‍💻 **Author** | [Karthika Krishna M (KK)](https://github.com/KARTHIKAKRISHNA123) |

---

## What I Built

The work is split into two parts. `ai_agents/` is agent logic written from scratch, and `frameworks/` is the same ideas rebuilt with production frameworks.

### 🤖 Part 1: AI Agents from scratch (`ai_agents/`)

Plain Python and the `ollama` client, with no frameworks. The aim was to understand what an agent really is before using a library that hides it.

| File | What it does |
|---|---|
| `hello.py` | First call to a local model: one prompt, one reply |
| `chatbot.py` | Interactive chat loop with a question counter (TinyLlama) |
| `memory_chatbot.py` | Keeps the full conversation history so the model remembers earlier turns, with a `history` command |
| `techbot.py` | A persona-driven study assistant, shaped with a system prompt |
| `react_agent.py` | **ReAct** pattern: forces Thought → Plan → Action → Final Answer on every question |
| `rewoo_agents.py` | **ReWOO** pattern: a planner makes the steps first, then they are executed and combined |
| `tool_agent.py` | Tool-calling agent with functions for time, math and more, chosen by the model |

### 🧩 Part 2: Frameworks (`frameworks/`)

| Folder | Focus | Highlights |
|---|---|---|
| `langchain-demo/` | LangChain fundamentals | Models, prompt templates, output parsers (structured JSON with Pydantic), LCEL chains (`prompt \| llm \| parser`), custom `@tool`s, and an agent that uses a calculator and a student lookup |
| `langgraph-demo/` | Stateful agent graphs | A first `StateGraph`, an **AI customer-support router**, and a capstone **multi-agent university assistant** whose memory persists in SQLite between runs |
| `hr-assistant/` | RAG over company documents | HR policy, leave policy and handbook indexed into a **FAISS** vector store, plus an agent that answers questions from them |
| `mcp/` | Model Context Protocol | MCP basics → tool registry and discovery → a real **MCP server** exposing live-data tools → an **agent client** that discovers and calls those tools over stdio |

---

## How the Pieces Fit

```
ai_agents/                 →  Understand the loop: prompt, reason, act
        │
        ▼
frameworks/langchain-demo  →  Reusable building blocks: prompts, parsers, tools
        │
        ▼
frameworks/langgraph-demo  →  Stateful workflows: routing, memory, multi-agent
        │
        ├── hr-assistant   →  Ground answers in documents (RAG + FAISS)
        └── mcp            →  Connect agents to external tools via a standard protocol
```

---

## Project Structure

```
tnsdc-ibm-adroit-internship/
├── ai_agents/
│   ├── hello.py
│   ├── chatbot.py
│   ├── memory_chatbot.py
│   ├── techbot.py
│   ├── react_agent.py
│   ├── rewoo_agents.py
│   └── tool_agent.py
├── frameworks/
│   ├── requirements.txt
│   ├── langchain-demo/
│   │   ├── models.py · promptTemplates.py · parsers.py
│   │   ├── lcel.py · customtools.py · agentLab.py
│   ├── langgraph-demo/
│   │   ├── simple_greeting_stategraph.py
│   │   ├── ai_customer_support_router.py
│   │   └── persistent_memory_clg_agent.py
│   ├── hr-assistant/
│   │   ├── vector-db.py · hr_agent.py
│   │   └── Employee_HandBook.txt · Leave_Policy.txt · PythonDeveloperJobDescription.txt
│   └── mcp/
│       ├── mcp1.py · mcp2.py
│       ├── mcpServer.py · Agent_Client.py
│       └── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Install Ollama and pull the models

Install Ollama from [ollama.com](https://ollama.com), then:

```bash
ollama pull tinyllama
ollama pull qwen2.5:3b
```

### 2. Clone the repo and create a virtual environment

```bash
git clone https://github.com/KARTHIKAKRISHNA123/tnsdc-ibm-adroit-internship.git
cd tnsdc-ibm-adroit-internship

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
# Part 1 (from-scratch agents)
pip install ollama

# Part 2 (frameworks)
pip install -r frameworks/requirements.txt

# MCP demos
pip install -r frameworks/mcp/requirements.txt requests
```

### 4. Run something

```bash
# A memory-enabled chatbot
python ai_agents/memory_chatbot.py

# The ReAct reasoning agent
python ai_agents/react_agent.py

# The multi-agent university assistant (LangGraph + SQLite memory)
cd frameworks/langgraph-demo
python persistent_memory_clg_agent.py
```

**Running the RAG assistant** (build the index first, then chat):

```bash
cd frameworks/hr-assistant
python vector-db.py     # builds the FAISS index from the .txt documents
python hr_agent.py      # asks questions against them
```

> **Note on the MCP client:** `Agent_Client.py` launches the server as `mcp_server.py`, while the file in this repo is named `mcpServer.py`. Either rename the file to `mcp_server.py` or update `SERVER_PARAMS` in `Agent_Client.py` before running it.

---

## Key Concepts Learned

| Concept | Where to see it |
|---|---|
| Prompting and system prompts | `techbot.py`, `promptTemplates.py` |
| Conversation memory | `memory_chatbot.py`, `persistent_memory_clg_agent.py` |
| ReAct (reason + act) | `react_agent.py` |
| ReWOO (plan first, then execute) | `rewoo_agents.py` |
| Tool / function calling | `tool_agent.py`, `customtools.py`, `agentLab.py` |
| Structured output | `parsers.py` (Pydantic + JSON) |
| LCEL chains | `lcel.py` |
| Stateful graphs and routing | `frameworks/langgraph-demo/` |
| Retrieval-Augmented Generation | `frameworks/hr-assistant/` |
| Model Context Protocol | `frameworks/mcp/` |

---

## Tech Stack

<p>
  <img src="https://skillicons.dev/icons?i=python,sqlite,git,github,vscode&theme=dark" />
</p>

`Ollama` · `LangChain` · `LangGraph` · `FAISS` · `ChromaDB` · `MCP` · `Pydantic` · `SQLAlchemy` · `Rich`

---

## Why Local Models?

- **Free and private.** Nothing leaves the machine, and there are no API keys to leak.
- **Forces good engineering.** A 3B model can't hide a sloppy prompt, so structure, parsing and tool design have to be right.
- **Works offline.** The whole stack runs on a normal laptop.

---

## Acknowledgements

- **TNSDC** (Tamil Nadu Skill Development Corporation) and **IBM** for the programme
- **Adroit Technologies** for delivering the training
- The Ollama, LangChain, LangGraph and MCP open-source communities

---

<div align="center">

### 👩‍💻 Author

**Karthika Krishna M (KK)** · CSE student, Anna University Regional Campus, Tirunelveli

[![GitHub](https://img.shields.io/badge/GitHub-KARTHIKAKRISHNA123-6C63FF?style=for-the-badge&logo=github&logoColor=white)](https://github.com/KARTHIKAKRISHNA123)

⭐ If this helped you learn about agents, consider starring the repo.

<img src="https://capsule-render.vercel.app/api?type=waving&color=6C63FF&height=100&section=footer"/>

</div>
