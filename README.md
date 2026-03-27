# Maison Beauté AI Advisor

> Privacy-First AI for Pre-Loved Luxury Beauty  
> Ironhack AI Consulting & Integration Bootcamp — Capstone Project  
> Student: Carolina

---

## Overview

A three-module AI system built for Maison Beauté, a pre-loved luxury beauty marketplace based in Berlin.

| Module | Name | Description |
|---|---|---|
| M1 | Shop Manager Agent | Auto-generates SEO-optimised product descriptions from JSON product data |
| M2 | Beauty Advisor Chatbot | RAG-powered beauty advisor with hard-wired allergy/safety escalation |
| M3 | Order Concierge | Order tracking via order number only — zero PII in chat |

---

## Tech Stack

- **LLM:** Claude Haiku (`claude-haiku-4-5-20251001`) via Anthropic API
- **Embeddings:** `text-embedding-3-small` via OpenAI API
- **Framework:** LangChain + LangGraph
- **RAG:** FAISS vector store
- **Observability:** LangSmith → Tableau
- **Orchestration:** n8n Cloud
- **Backend:** Python 3.13 + FastAPI

---

## Project Structure

```
maison-beaute-ai-advisor/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── core/
│   │   ├── langsmith_config.py  # LangSmith setup
│   │   ├── rag_pipeline.py      # FAISS RAG chain (Module 2)
│   │   └── langgraph_agent.py   # Safety routing agent (Module 2)
│   ├── routers/
│   │   ├── descriptions.py      # Module 1 endpoints
│   │   ├── chatbot.py           # Module 2 endpoints
│   │   └── orders.py            # Module 3 endpoints
│   └── models/
│       ├── product.py           # Pydantic models — product data
│       └── chat.py              # Pydantic models — chat session
├── n8n/
│   ├── workflow_module1_descriptions.json
│   ├── workflow_module2_chatbot.json
│   └── workflow_module3_orders.json
├── data/
│   ├── product_catalogue_sample.json
│   ├── faq_knowledge_base.md
│   └── policies.md
├── evals/
│   ├── langsmith_eval_config.py
│   ├── export_to_tableau.py
│   └── test_cases.json
├── docs/
│   ├── EU_AI_Act_Conformity_Assessment.md
│   ├── GDPR_DPIA.md
│   └── Architecture_Diagram.md
├── jira/
│   └── sprint_board_export.json
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/your-username/maison-beaute-ai-advisor.git
cd maison-beaute-ai-advisor

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# → Open .env and add your API keys

# 5. Run the API
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key (Claude Haiku) |
| `OPENAI_API_KEY` | OpenAI API key (embeddings only) |
| `LANGCHAIN_API_KEY` | LangSmith API key |
| `LANGCHAIN_PROJECT` | LangSmith project name |
| `N8N_WEBHOOK_BASE_URL` | Your n8n Cloud instance base URL |
| `FULFILMENT_API_URL` | Internal order fulfilment API |
| `CATALOGUE_API_URL` | Internal product catalogue API |

---

## Compliance

- **EU AI Act:** Limited Risk (Article 50) — transparency obligations only
- **GDPR:** Privacy-by-design architecture — zero PII in chat responses
- See `docs/` for full compliance documentation

---

## Observability

LangSmith traces all LLM calls across all three modules.  
Export to Tableau via `evals/export_to_tableau.py` for the operations dashboard.

---

*Maison Beauté AI Advisor — Ironhack Berlin, 2024*
