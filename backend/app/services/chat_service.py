from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..models.chat import ChatHistory
from ..schemas.chat import ChatRequest, ChatResponse, ChatHistoryItem
import sys
from pathlib import Path
import uuid

# agent 모듈 import를 위한 경로 추가
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from agent.graph import agent
from agent.memory import memory_manager


class ChatService:
    """챗봇 서비스"""

    async def process_question(
        self,
        db: Session,
        request: ChatRequest
    ) -> ChatResponse:
        """질문 처리"""
        # 세션 ID가 없으면 생성
        session_id = request.session_id or str(uuid.uuid4())

        # Agent로 질문 처리
        result = await agent.run(request.question, session_id)

        # 데이터베이스에 저장
        chat_history = ChatHistory(
            session_id=session_id,
            question=request.question,
            answer=result["answer"]
        )
        db.add(chat_history)
        db.commit()

        # 메모리에도 저장
        memory_manager.save_conversation(
            session_id,
            request.question,
            result["answer"]
        )

        return ChatResponse(
            answer=result["answer"],
            session_id=session_id,
            timestamp=datetime.now()
        )

    def get_chat_history(
        self,
        db: Session,
        session_id: str
    ) -> List[ChatHistory]:
        """대화 이력 조회"""
        return db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.timestamp).all()


chat_service = ChatService()
