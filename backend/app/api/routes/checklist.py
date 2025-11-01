from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...schemas.checklist import ChecklistResponse, ChecklistItemResponse, ChecklistItemUpdate
from ...services.checklist_service import checklist_service
from ..dependencies import get_session_id

router = APIRouter(prefix="/api", tags=["checklist"])


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
