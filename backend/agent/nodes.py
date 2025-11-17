from typing import Dict, Any, TypedDict
from .tools import search_tools
import google.generativeai as genai
import os


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
    """응답 생성 노드 (Gemini AI 사용)"""
    question = state.get("question", "")
    search_results = state.get("search_results", [])

    # Gemini API 설정
    api_key = os.getenv("GEMINI_API_KEY", "")

    # API 키가 있고 유효한 경우 Gemini 사용
    if api_key and api_key != "dummy_gemini_api_key" and len(api_key) > 20:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # 프롬프트 구성
            context = ""
            if search_results:
                context = "\n".join([f"- {r.get('info', '')}" for r in search_results])

            prompt = f"""당신은 1인 가구 이사를 도와주는 친절한 AI 어시스턴트입니다.

사용자 질문: {question}

{f'참고 정보:{context}' if context else ''}

위 질문에 대해 친절하고 구체적으로 답변해주세요. 이사 관련 실용적인 조언을 제공하되, 간결하게 2-3문장으로 답변해주세요."""

            response = model.generate_content(prompt)
            answer = response.text.strip()

        except Exception as e:
            print(f"Gemini API 오류: {e}")
            # 오류 발생 시 기본 답변 사용
            if search_results:
                answer = search_results[0].get("info", "죄송합니다. 관련 정보를 찾을 수 없습니다.")
            else:
                answer = "이사 관련 질문에 대해 더 구체적으로 말씀해 주시면 도와드리겠습니다."
    else:
        # API 키가 없으면 기본 지식 베이스 사용
        if search_results:
            answer = search_results[0].get("info", "죄송합니다. 관련 정보를 찾을 수 없습니다.")
        else:
            answer = "이사 관련 질문에 대해 더 구체적으로 말씀해 주시면 도와드리겠습니다."

    return {
        **state,
        "answer": answer
    }
