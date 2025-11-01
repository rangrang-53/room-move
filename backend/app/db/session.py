from sqlalchemy.orm import Session
from .database import SessionLocal


def get_session() -> Session:
    """세션 생성 헬퍼 함수"""
    return SessionLocal()
