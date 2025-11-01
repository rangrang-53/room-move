from pydantic import BaseModel, Field
from datetime import date


class DdayRequest(BaseModel):
    """D-day 계산 요청 스키마"""
    move_date: date = Field(..., description="이사 날짜 (YYYY-MM-DD)")


class DdayResponse(BaseModel):
    """D-day 계산 응답 스키마"""
    d_day: int = Field(..., description="D-day (음수는 지난 날짜)")
    move_date: str = Field(..., description="이사 날짜")
    current_date: str = Field(..., description="현재 날짜")
    message: str = Field(..., description="안내 메시지")
