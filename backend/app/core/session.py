from itsdangerous import URLSafeTimedSerializer
from .config import settings


class SessionManager:
    """세션 관리자"""

    def __init__(self):
        self.serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

    def create_session_id(self, data: dict) -> str:
        """세션 ID 생성"""
        return self.serializer.dumps(data)

    def validate_session_id(self, session_id: str, max_age: int = 3600) -> dict:
        """세션 ID 검증"""
        try:
            return self.serializer.loads(session_id, max_age=max_age)
        except Exception:
            return None


session_manager = SessionManager()
