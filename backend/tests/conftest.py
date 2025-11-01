import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
import app.db.database as database_module

# 모든 모델 import (테스트 DB 테이블 생성을 위해 필수)
from app.models.checklist import ChecklistItem
from app.models.movers import Mover
from app.models.chat import ChatHistory

# 테스트용 인메모리 데이터베이스
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """테스트용 DB 세션"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """각 테스트마다 새로운 DB 생성"""
    # 테스트용 엔진으로 테이블 생성
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """테스트 클라이언트"""
    # 프로덕션 엔진을 테스트 엔진으로 임시 교체
    original_engine = database_module.engine
    original_session_local = database_module.SessionLocal

    database_module.engine = engine
    database_module.SessionLocal = TestingSessionLocal

    # app을 import해서 startup 이벤트가 테스트 DB를 사용하도록 함
    from app.main import app
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # 원래대로 복구
    app.dependency_overrides.clear()
    database_module.engine = original_engine
    database_module.SessionLocal = original_session_local
