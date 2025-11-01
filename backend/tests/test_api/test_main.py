import pytest


def test_root_endpoint(client):
    """루트 엔드포인트 테스트"""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "RoomMove" in data["message"]
    assert "version" in data


def test_health_check(client):
    """헬스 체크 엔드포인트 테스트"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
