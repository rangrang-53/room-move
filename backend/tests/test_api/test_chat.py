import pytest


def test_send_chat_message(client):
    """챗봇 메시지 전송 테스트"""
    response = client.post(
        "/api/chat",
        json={
            "question": "전입신고는 언제 해야 하나요?",
            "session_id": "test-session-123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "session_id" in data
    assert "timestamp" in data
    assert len(data["answer"]) > 0


def test_chat_knowledge_base(client):
    """지식 베이스 응답 테스트"""
    # 전입신고 관련 질문
    response = client.post(
        "/api/chat",
        json={
            "question": "전입신고 언제 하나요?",
            "session_id": "test-session-456"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "14일" in data["answer"]


def test_get_chat_history(client):
    """대화 이력 조회 테스트"""
    session_id = "test-session-789"

    # 먼저 메시지 전송
    client.post(
        "/api/chat",
        json={
            "question": "이삿짐은 언제 예약하나요?",
            "session_id": session_id
        }
    )

    # 이력 조회
    response = client.get(f"/api/chat/history?session_id={session_id}")

    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert len(data["history"]) > 0


def test_get_chat_history_empty(client):
    """빈 대화 이력 조회 테스트"""
    response = client.get("/api/chat/history?session_id=nonexistent-session")

    assert response.status_code == 404
