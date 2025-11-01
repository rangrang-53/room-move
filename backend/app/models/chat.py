from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..db.database import Base


class ChatHistory(Base):
    """챗봇 대화 이력 모델"""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
