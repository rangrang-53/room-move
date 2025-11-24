from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from ...db.database import get_db
from ...schemas.checklist import ChecklistResponse, ChecklistItemResponse, ChecklistItemUpdate
from ...services.checklist_service import checklist_service
from ..dependencies import get_session_id

router = APIRouter(prefix="/api", tags=["checklist"])


class AutoCheckRequest(BaseModel):
    """자동 체크 요청"""
    message: str


class AutoCheckResponse(BaseModel):
    """자동 체크 응답"""
    checked_items: List[str]
    message: str


@router.get("/checklist", response_model=ChecklistResponse)
async def get_checklist(
    session_id: Optional[str] = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    체크리스트 조회 API

    전체 체크리스트 항목을 조회합니다.
    """
    items = checklist_service.get_all_items(db, session_id)
    return ChecklistResponse(checklist=items)


@router.put("/checklist/{item_id}", response_model=ChecklistItemResponse)
async def update_checklist_item(
    item_id: int,
    update_data: ChecklistItemUpdate,
    db: Session = Depends(get_db)
):
    """
    체크리스트 항목 업데이트 API

    특정 체크리스트 항목의 완료 여부를 업데이트합니다.
    """
    item = checklist_service.update_item(db, item_id, update_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.post("/checklist/auto-check", response_model=AutoCheckResponse)
async def auto_check_from_message(
    request: AutoCheckRequest,
    db: Session = Depends(get_db)
):
    """
    메시지에서 완료된 작업을 감지하여 자동으로 체크리스트 체크

    사용자가 "전입신고 했어" 같은 메시지를 보내면 해당 항목을 자동으로 체크합니다.
    """
    # 메시지에서 완료된 작업 감지
    detected_tasks = checklist_service.detect_completed_tasks(request.message)

    checked_items = []
    for task_keyword in detected_tasks:
        item = checklist_service.mark_item_completed_by_keyword(db, task_keyword)
        if item:
            checked_items.append(item.title)

    if checked_items:
        message = f"'{', '.join(checked_items)}' 항목을 완료 처리했습니다."
    else:
        message = ""

    return AutoCheckResponse(checked_items=checked_items, message=message)
