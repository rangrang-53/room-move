from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import os
from ..models.movers import Mover


class MoversService:
    """이삿짐 센터 서비스"""

    def __init__(self):
        self.data_file = "backend/data/movers.csv"

    def get_all_movers(self, db: Session, region: Optional[str] = None) -> List[Mover]:
        """모든 이삿짐 센터 조회 (지역 필터링 가능)"""
        # 데이터베이스에서 조회
        query = db.query(Mover)

        # 지역 필터링
        if region:
            query = query.filter(Mover.region.like(f"%{region}%"))

        movers = query.all()

        # DB에 데이터가 없으면 CSV 파일에서 로드
        if not movers:
            movers = self._load_from_csv(db, region)

        return movers

    def get_mover_by_id(self, db: Session, mover_id: int) -> Optional[Mover]:
        """ID로 이삿짐 센터 조회"""
        return db.query(Mover).filter(Mover.id == mover_id).first()

    def _load_from_csv(self, db: Session, region: Optional[str] = None) -> List[Mover]:
        """CSV 파일에서 이삿짐 센터 로드"""
        if not os.path.exists(self.data_file):
            return []

        # pandas로 CSV 읽기
        df = pd.read_csv(self.data_file)

        movers = []
        for _, row in df.iterrows():
            # 지역 필터링
            if region and region not in str(row['region']):
                continue

            mover = Mover(
                name=row['name'],
                region=row['region'],
                phone=row['phone'],
                price=int(row['price']),
                description=row.get('description', '')
            )
            db.add(mover)
            movers.append(mover)

        db.commit()
        return movers


movers_service = MoversService()
