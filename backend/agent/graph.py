from typing import Dict, Any
from .nodes import (
    AgentState,
    question_understanding_node,
    search_node,
    answer_generation_node
)


class SimpleAgent:
    """간단한 Agent 시스템 (LangGraph 대체)"""

    async def run(self, question: str, session_id: str = "") -> Dict[str, Any]:
        """Agent 실행"""

        # 초기 상태
        state: AgentState = {
            "question": question,
            "search_results": [],
            "answer": "",
            "session_id": session_id
        }

        # 노드 실행
        state = await question_understanding_node(state)
        state = await search_node(state)
        state = await answer_generation_node(state)

        return {
            "question": state["question"],
            "answer": state["answer"],
            "session_id": state["session_id"]
        }


# Agent 인스턴스
agent = SimpleAgent()
