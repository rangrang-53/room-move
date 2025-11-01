from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from ...services.chat_service import chat_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def process_chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    챗봇 질문 처리 API

    사용자의 질문을 Agent가 처리하고 응답을 반환합니다.
    """
    return await chat_service.process_question(db, request)


@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    챗봇 대화 이력 조회 API

    특정 세션의 대화 이력을 조회합니다.
    """
    history = chat_service.get_chat_history(db, session_id)

    if not history:
        raise HTTPException(status_code=404, detail="No chat history found")

    return ChatHistoryResponse(
        history=history,
        session_id=session_id
    )
