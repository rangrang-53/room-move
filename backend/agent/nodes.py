from typing import Dict, Any, TypedDict
from .tools import search_tools


class AgentState(TypedDict):
    """Agent 상태 타입"""
    question: str
    search_results: list
    answer: str
    session_id: str


async def question_understanding_node(state: AgentState) -> AgentState:
    """질문 이해 노드"""
    question = state.get("question", "")

    # 간단한 질문 전처리
    processed_question = question.strip()

    return {
        **state,
        "question": processed_question
    }


async def search_node(state: AgentState) -> AgentState:
    """정보 검색 노드"""
    question = state.get("question", "")

    # 이사 관련 기본 지식 베이스
    knowledge_base = {
        "전입신고": "전입신고는 이사 후 14일 이내에 하셔야 합니다. 주민센터 방문 또는 정부24 온라인으로 신청 가능합니다.",
        "이삿짐": "이삿짐 센터는 최소 1주일 전에 예약하시는 것이 좋습니다. 주말이나 월말에는 더 일찍 예약해야 합니다.",
        "공공요금": "이사 전에 전기, 가스, 수도 요금을 정산하고 해지 신청을 해야 합니다.",
        "인터넷": "인터넷과 TV는 이사 2주 전에 해지 또는 이전 신청을 하는 것이 좋습니다."
    }

    # 키워드 매칭으로 답변 찾기
    results = []
    for keyword, info in knowledge_base.items():
        if keyword in question:
            results.append({"keyword": keyword, "info": info})

    # 검색 결과가 없으면 외부 API 호출 (현재는 스킵)
    if not results:
        # naver_results = await search_tools.naver_search(question)
        # exa_results = await search_tools.exa_search(question)
        results.append({
            "keyword": "기본",
            "info": "이사 관련 정보는 정부24 또는 주민센터에 문의하시면 자세히 안내받으실 수 있습니다."
        })

    return {
        **state,
        "search_results": results
    }


async def answer_generation_node(state: AgentState) -> AgentState:
    """응답 생성 노드"""
    search_results = state.get("search_results", [])

    # 검색 결과를 바탕으로 답변 생성
    if search_results:
        answer = search_results[0].get("info", "죄송합니다. 관련 정보를 찾을 수 없습니다.")
    else:
        answer = "이사 관련 질문에 대해 더 구체적으로 말씀해 주시면 도와드리겠습니다."

    return {
        **state,
        "answer": answer
    }
