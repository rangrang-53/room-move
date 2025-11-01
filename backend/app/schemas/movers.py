from pydantic import BaseModel, Field
from typing import Optional


class MoverBase(BaseModel):
    """이삿짐 센터 기본 스키마"""
    name: str = Field(..., description="업체명")
    region: str = Field(..., description="지역")
    phone: str = Field(..., description="연락처")
    price: int = Field(..., description="예상 금액")
    description: Optional[str] = Field(None, description="업체 설명")


class MoverResponse(MoverBase):
    """이삿짐 센터 응답 스키마"""
    id: int = Field(..., description="업체 ID")

    class Config:
        from_attributes = True


class MoversResponse(BaseModel):
    """이삿짐 센터 목록 응답 스키마"""
    movers: list[MoverResponse] = Field(..., description="이삿짐 센터 목록")
    region: Optional[str] = Field(None, description="필터링된 지역")
