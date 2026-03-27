# System Architecture

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    MAISON BEAUTÉ AI SYSTEM                   │
├─────────────────────┬─────────────────────┬─────────────────┤
│   MODULE 1          │   MODULE 2           │   MODULE 3      │
│   Shop Manager      │   Beauty Advisor     │   Order         │
│   Agent             │   Chatbot            │   Concierge     │
├─────────────────────┼─────────────────────┼─────────────────┤
│ POST /products/     │ POST /chat/          │ POST /orders/   │
│ generate-description│                      │ track           │
│                     │                      │                 │
│ ProductInput JSON   │ message + session_id │ order_number    │
│       ↓             │       ↓              │       ↓         │
│ Claude Haiku        │ Safety keyword scan  │ Fulfilment API  │
│ (copywriter prompt) │       ↓              │       ↓         │
│       ↓             │ Flag? → Escalate     │ Brief status    │
│ ProductDescription  │ No?  → RAG + Haiku   │ Email via MCP   │
│ JSON published      │       ↓              │ (no PII shown)  │
│ + MCP Slack notify  │ ChatResponse         │ OrderResponse   │
└─────────────────────┴─────────────────────┴─────────────────┘
                                │
                    ┌───────────────────────┐
                    │   SHARED INFRA         │
                    │ LangChain + LangGraph  │
                    │ FAISS vector store     │
                    │ LangSmith → Tableau    │
                    │ n8n Cloud (MCP)        │
                    │ GitHub + FastAPI       │
                    └───────────────────────┘
```

## Data Flow — Module 2 Safety Escalation

```
Customer message
       │
       ▼
Safety keyword scan (local, n8n Code Node)
       │
  Flag detected?
  ┌────┴────┐
 YES       NO
  │         │
  ▼         ▼
Slack     RAG retrieval
alert     (FAISS → top 4 chunks)
  │         │
  ▼         ▼
Safe      Claude Haiku
holding   response
response
```

## Data Flow — Module 3 Privacy Design

```
Input:  order_number only
           │
           ▼
  Internal fulfilment DB
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
Brief status   Email (on file)
→ chat         → full details
  (no PII)       via MCP
```
