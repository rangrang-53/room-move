from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...schemas.movers import MoversResponse
from ...services.movers_service import movers_service

router = APIRouter(prefix="/api", tags=["movers"])


@router.get("/movers", response_model=MoversResponse)
async def get_movers(
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    이삿짐 센터 조회 API

    전체 이삿짐 센터 목록을 조회합니다.
    region 파라미터로 지역별 필터링이 가능합니다.
    """
    movers = movers_service.get_all_movers(db, region)
    return MoversResponse(movers=movers, region=region)
