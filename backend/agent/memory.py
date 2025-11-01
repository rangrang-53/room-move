from typing import Dict, List
from collections import defaultdict


class MemoryManager:
    """메모리 관리자 (로컬 인메모리)"""

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def save_conversation(self, session_id: str, question: str, answer: str):
        """대화 저장"""
        self.conversations[session_id].append({
            "question": question,
            "answer": answer
        })

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """대화 이력 조회"""
        return self.conversations.get(session_id, [])

    def clear_conversation(self, session_id: str):
        """대화 이력 삭제"""
        if session_id in self.conversations:
            del self.conversations[session_id]


# 메모리 관리자 인스턴스
memory_manager = MemoryManager()
