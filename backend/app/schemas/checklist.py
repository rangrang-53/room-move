from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChecklistItemBase(BaseModel):
    """체크리스트 기본 스키마"""
    title: str = Field(..., description="항목 제목")
    description: Optional[str] = Field(None, description="항목 설명")
    completed: bool = Field(False, description="완료 여부")


class ChecklistItemCreate(ChecklistItemBase):
    """체크리스트 생성 스키마"""
    pass


class ChecklistItemUpdate(BaseModel):
    """체크리스트 업데이트 스키마"""
    completed: bool = Field(..., description="완료 여부")


class ChecklistItemResponse(ChecklistItemBase):
    """체크리스트 응답 스키마"""
    id: int = Field(..., description="항목 ID")
    updated_at: Optional[datetime] = Field(None, description="업데이트 시간")

    class Config:
        from_attributes = True


class ChecklistResponse(BaseModel):
    """체크리스트 목록 응답 스키마"""
    checklist: list[ChecklistItemResponse] = Field(..., description="체크리스트 목록")
