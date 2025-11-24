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
        # 데이터베이스에서 조회 (session_id 필터링 제거 - 체크리스트는 전역 항목)
        items = db.query(ChecklistItem).all()

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

    def find_item_by_keyword(self, db: Session, keyword: str) -> Optional[ChecklistItem]:
        """키워드로 체크리스트 항목 찾기"""
        items = db.query(ChecklistItem).all()
        keyword_lower = keyword.lower()

        for item in items:
            # 제목에 키워드가 포함되어 있는지 확인
            if keyword_lower in item.title.lower():
                return item
        return None

    def mark_item_completed_by_keyword(self, db: Session, keyword: str) -> Optional[ChecklistItem]:
        """키워드로 항목을 찾아서 완료 처리"""
        item = self.find_item_by_keyword(db, keyword)
        if item and not item.completed:
            item.completed = True
            db.commit()
            db.refresh(item)
            return item
        return None

    def detect_completed_tasks(self, message: str) -> List[str]:
        """메시지에서 완료된 작업 감지"""
        # 완료를 나타내는 패턴들
        completed_patterns = [
            "했어", "했습니다", "완료", "끝났", "마쳤", "처리했", "신청했", "예약했",
            "정산했", "해지했", "확인했", "받았", "정리했", "청소했"
        ]

        # 체크리스트 항목 키워드 매핑
        checklist_keywords = {
            "전입신고": ["전입신고", "전입 신고", "주민등록"],
            "인터넷": ["인터넷", "TV", "티비", "케이블"],
            "공공요금": ["공공요금", "전기", "가스", "수도", "요금"],
            "이삿짐": ["이삿짐", "이사짐", "이삿짐센터", "이사업체", "포장이사"],
            "청소": ["청소", "정리"],
            "우편물": ["우편물", "우편", "주소변경"],
            "보증금": ["보증금", "월세", "전세금", "반환"]
        }

        detected = []
        message_lower = message.lower()

        # 완료 패턴이 있는지 확인
        has_completion = any(pattern in message for pattern in completed_patterns)

        if has_completion:
            for category, keywords in checklist_keywords.items():
                for kw in keywords:
                    if kw in message:
                        detected.append(category)
                        break

        return list(set(detected))

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
