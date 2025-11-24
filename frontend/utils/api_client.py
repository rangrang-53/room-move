import requests
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    """백엔드 API 클라이언트"""

    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.session_id: Optional[str] = None

    def set_session_id(self, session_id: str):
        """세션 ID 설정"""
        self.session_id = session_id

    def _get_headers(self) -> Dict[str, str]:
        """요청 헤더 생성"""
        headers = {"Content-Type": "application/json"}
        if self.session_id:
            headers["x-session-id"] = self.session_id
        return headers

    # D-day API
    def calculate_dday(self, move_date: str) -> Dict[str, Any]:
        """D-day 계산"""
        try:
            response = requests.post(
                f"{self.base_url}/api/dday",
                json={"move_date": move_date},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # Checklist API
    def get_checklist(self) -> Dict[str, Any]:
        """체크리스트 조회"""
        try:
            url = f"{self.base_url}/api/checklist"
            headers = self._get_headers()
            print(f"DEBUG - Requesting URL: {url}")
            print(f"DEBUG - Headers: {headers}")

            response = requests.get(url, headers=headers)
            print(f"DEBUG - Status Code: {response.status_code}")
            print(f"DEBUG - Response Text: {response.text[:500]}")  # 처음 500자만

            response.raise_for_status()
            data = response.json()
            print(f"DEBUG - Parsed JSON keys: {data.keys()}")
            print(f"DEBUG - Checklist length: {len(data.get('checklist', []))}")
            return data
        except Exception as e:
            print(f"DEBUG - Exception: {type(e).__name__}: {e}")
            return {"error": str(e)}

    def update_checklist_item(self, item_id: int, completed: bool) -> Dict[str, Any]:
        """체크리스트 항목 업데이트"""
        try:
            response = requests.put(
                f"{self.base_url}/api/checklist/{item_id}",
                json={"completed": completed},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def auto_check_from_message(self, message: str) -> Dict[str, Any]:
        """메시지에서 완료된 작업을 감지하여 자동 체크"""
        try:
            response = requests.post(
                f"{self.base_url}/api/checklist/auto-check",
                json={"message": message},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # Movers API
    def get_movers(self, region: Optional[str] = None) -> Dict[str, Any]:
        """이삿짐 센터 조회"""
        try:
            params = {"region": region} if region else {}
            response = requests.get(
                f"{self.base_url}/api/movers",
                params=params,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # Chat API
    def send_chat_message(self, question: str) -> Dict[str, Any]:
        """챗봇 메시지 전송"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={"question": question, "session_id": self.session_id},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_chat_history(self) -> Dict[str, Any]:
        """챗봇 대화 이력 조회"""
        if not self.session_id:
            return {"error": "No session ID"}

        try:
            response = requests.get(
                f"{self.base_url}/api/chat/history",
                params={"session_id": self.session_id},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# API 클라이언트 인스턴스
api_client = APIClient()
