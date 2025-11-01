import pytest


def test_get_all_movers(client):
    """전체 이삿짐 센터 조회 테스트"""
    response = client.get("/api/movers")

    assert response.status_code == 200
    data = response.json()
    assert "movers" in data
    assert isinstance(data["movers"], list)


def test_get_movers_by_region(client):
    """지역별 이삿짐 센터 조회 테스트"""
    response = client.get("/api/movers?region=서울 강남구")

    assert response.status_code == 200
    data = response.json()
    assert "movers" in data
    assert data["region"] == "서울 강남구"

    # 모든 업체가 해당 지역인지 확인
    for mover in data["movers"]:
        assert "강남구" in mover["region"]


def test_get_movers_empty_region(client):
    """존재하지 않는 지역 조회 테스트"""
    response = client.get("/api/movers?region=존재하지않는지역")

    assert response.status_code == 200
    data = response.json()
    assert len(data["movers"]) == 0
