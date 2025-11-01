from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from ..models.checklist import ChecklistItem
from ..schemas.checklist import ChecklistItemUpdate


class ChecklistService:
    """체크리스트 서비스"""

    def __init__(self):
        self.data_file = "backend/data/checklist.json"

    def get_all_items(self, db: Session, session_id: Optional[str] = None) -> List[ChecklistItem]:
        """모든 체크리스트 항목 조회"""
        # 데이터베이스에서 조회
        query = db.query(ChecklistItem)
        if session_id:
            query = query.filter(ChecklistItem.session_id == session_id)

        items = query.all()

        # DB에 데이터가 없으면 JSON 파일에서 로드
        if not items:
            items = self._load_from_json(db, session_id)

        return items

    def get_item_by_id(self, db: Session, item_id: int) -> Optional[ChecklistItem]:
        """ID로 체크리스트 항목 조회"""
        return db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()

    def update_item(
        self,
        db: Session,
        item_id: int,
        update_data: ChecklistItemUpdate
    ) -> Optional[ChecklistItem]:
        """체크리스트 항목 업데이트"""
        item = self.get_item_by_id(db, item_id)
        if not item:
            return None

        item.completed = update_data.completed
        db.commit()
        db.refresh(item)
        return item

    def _load_from_json(self, db: Session, session_id: Optional[str] = None) -> List[ChecklistItem]:
        """JSON 파일에서 체크리스트 로드"""
        if not os.path.exists(self.data_file):
            return []

        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = []
        for item_data in data:
            item = ChecklistItem(
                title=item_data["title"],
                description=item_data.get("description"),
                completed=item_data.get("completed", False),
                session_id=session_id
            )
            db.add(item)
            items.append(item)

        db.commit()
        return items


checklist_service = ChecklistService()
