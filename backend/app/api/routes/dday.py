from fastapi import APIRouter
from ...schemas.dday import DdayRequest, DdayResponse
from ...services.dday_service import dday_service

router = APIRouter(prefix="/api", tags=["dday"])


@router.post("/dday", response_model=DdayResponse)
async def calculate_dday(request: DdayRequest):
    """
    D-day 계산 API

    이사 날짜를 입력받아 현재 날짜와의 차이를 계산합니다.
    """
    return dday_service.calculate_dday(request)
