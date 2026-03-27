# app/routers/chatbot.py
from fastapi import APIRouter, HTTPException
from langsmith import traceable

from app.core.langgraph_agent import agent
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
@traceable(name="chatbot_endpoint", tags=["module-2"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Module 2 — Beauty Advisor Chatbot.

    Flow:
    1. Safety check (keyword scan) — runs BEFORE any LLM call
    2a. If safety flag → escalate to founder via MCP Slack alert, return holding message
    2b. If no flag → RAG retrieval + Claude Haiku response

    Zero PII required from the customer.
    """
    try:
        initial_state = {
            "message": request.message,
            "session_id": request.session_id,
            "chat_history": [
                {"role": m.role, "content": m.content}
                for m in request.chat_history
            ],
            "safety_flagged": False,
            "response": "",
        }

        result = agent.invoke(initial_state)

        return ChatResponse(
            session_id=request.session_id,
            response=result["response"],
            safety_flagged=result["safety_flagged"],
            escalated=result["safety_flagged"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
