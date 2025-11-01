from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """챗봇 질문 요청 스키마"""
    question: str = Field(..., description="질문 내용")
    session_id: Optional[str] = Field(None, description="세션 ID")


class ChatResponse(BaseModel):
    """챗봇 응답 스키마"""
    answer: str = Field(..., description="응답 내용")
    session_id: str = Field(..., description="세션 ID")
    timestamp: datetime = Field(..., description="응답 시간")


class ChatHistoryItem(BaseModel):
    """챗봇 대화 이력 아이템"""
    question: str = Field(..., description="질문")
    answer: str = Field(..., description="응답")
    timestamp: datetime = Field(..., description="시간")

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """챗봇 대화 이력 응답 스키마"""
    history: list[ChatHistoryItem] = Field(..., description="대화 이력")
    session_id: str = Field(..., description="세션 ID")
