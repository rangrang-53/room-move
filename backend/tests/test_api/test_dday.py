import pytest
from datetime import date, timedelta


def test_calculate_dday_future(client):
    """미래 날짜 D-day 계산 테스트"""
    future_date = (date.today() + timedelta(days=14)).isoformat()

    response = client.post(
        "/api/dday",
        json={"move_date": future_date}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["d_day"] == 14
    assert "남았습니다" in data["message"]


def test_calculate_dday_today(client):
    """오늘 날짜 D-day 계산 테스트"""
    today = date.today().isoformat()

    response = client.post(
        "/api/dday",
        json={"move_date": today}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["d_day"] == 0
    assert "오늘" in data["message"]


def test_calculate_dday_past(client):
    """과거 날짜 D-day 계산 테스트"""
    past_date = (date.today() - timedelta(days=7)).isoformat()

    response = client.post(
        "/api/dday",
        json={"move_date": past_date}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["d_day"] == -7
    assert "지났습니다" in data["message"]


def test_calculate_dday_invalid_format(client):
    """잘못된 날짜 형식 테스트"""
    response = client.post(
        "/api/dday",
        json={"move_date": "invalid-date"}
    )

    assert response.status_code == 422  # Validation error
