# ChatCircuit
<img width="952" height="240" alt="image" src="https://github.com/user-attachments/assets/aa858cc0-56b6-48b4-b4e5-cd34e1b863d8" />
<img width="955" height="430" alt="image" src="https://github.com/user-attachments/assets/85ffc0d7-1457-4258-b83a-7fddb4a13dd6" />


---

# 🧠 AI Automation Platform with MCP, LangChain, and LLM REST APIs

This project is an **end-to-end AI automation system**, not just another chatbot or LLM wrapper.

It combines:

* **local MCP Server**
* **LangChain agent tooling**
* **LLM via REST API**
* **FastAPI orchestration backend**
* **LangSmith tracing and observability**

to build a platform that can run **real tools, APIs, and automated workflows** using AI reasoning.

---

## 🚀 What this project does

This system enables an AI agent to:

* call **real tools via MCP Server**
* run **REST APIs programmatically**
* perform **multi-step workflows**
* reason over tool outputs
* maintain **state and context across requests**
* trace and debug using **LangSmith**

So instead of just generating text, the agent can:

✔️ trigger APIs
✔️ read/write data
✔️ call tools in sequence
✔️ automate backend tasks
✔️ observe all runs end-to-end

---

## ✨ Why this is NOT just an LLM wrapper

Most repos call an LLM and return text.

This project adds:

* 🖥️ **locally running MCP Server** exposing executable tools
* 🔗 **LangChain agents** with multi-step tool planning
* 🌐 **LLM integration over REST** (no SDK lock-in)
* 🧩 **dynamic plug-and-play tool registry**
* 🧭 **task-level reasoning and decision making**
* 🧠 **persistent conversation + context memory**
* 🔁 **retry, error handling, and failure recovery**
* 🔍 **LangSmith tracing for observability**

---

## 🛠 Tech Stack

* Python
* FastAPI
* Local MCP Server
* LangChain
* LLaMA (or other) LLM via REST API
* LangSmith monitoring
* Docker (optional)

---

## 🧭 High-Level Architecture

```
Client Request
      ↓
FastAPI Orchestration Layer
      ↓
LangChain Agent
      ↓
MCP Server  ←→  Tools / APIs
      ↓
LLM (REST Endpoint)
      ↓
LangSmith Tracing
```

---

## 🔧 Features

* ✅ Local MCP tool execution
* ✅ AI-driven workflow automation
* ✅ Multi-step tool calling
* ✅ REST-based LLM inference
* ✅ LangSmith tracing and logs
* ✅ Modular tool registry
* ✅ Extensible architecture
* ✅ Production-style backend patterns

---

## 🏁 Use-cases

This platform can be extended for:

* Jira automation
* GitHub issue/PR automation
* API testing & DevOps scripting
* backend process automation
* intelligent assistants with real actions


---

## 🚧 Roadmap

* add more MCP tools
* add UI panel
* add authentication
* extend agent capabilities
* advanced orchestration flows

---

## 🤝 Contributions

PRs, issues, and discussions are welcome!

---


