from fastapi import Header, HTTPException
from typing import Optional
from ..core.session import session_manager


async def get_session_id(
    x_session_id: Optional[str] = Header(None)
) -> Optional[str]:
    """세션 ID 의존성"""
    return x_session_id


async def verify_session(
    session_id: str = Header(alias="x-session-id")
) -> dict:
    """세션 검증 의존성"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID required")

    session_data = session_manager.validate_session_id(session_id)
    if not session_data:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return session_data
