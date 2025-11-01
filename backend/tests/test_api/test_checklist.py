import pytest


def test_get_checklist(client):
    """체크리스트 조회 테스트"""
    response = client.get("/api/checklist")

    assert response.status_code == 200
    data = response.json()
    assert "checklist" in data
    assert isinstance(data["checklist"], list)


def test_update_checklist_item(client):
    """체크리스트 항목 업데이트 테스트"""
    # 먼저 체크리스트 조회
    response = client.get("/api/checklist")
    assert response.status_code == 200
    checklist = response.json()["checklist"]

    if len(checklist) > 0:
        item_id = checklist[0]["id"]

        # 완료 상태로 업데이트
        update_response = client.put(
            f"/api/checklist/{item_id}",
            json={"completed": True}
        )

        assert update_response.status_code == 200
        updated_item = update_response.json()
        assert updated_item["completed"] is True


def test_update_nonexistent_checklist_item(client):
    """존재하지 않는 체크리스트 항목 업데이트 테스트"""
    response = client.put(
        "/api/checklist/99999",
        json={"completed": True}
    )

    assert response.status_code == 404
