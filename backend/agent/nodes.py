from typing import Dict, Any, TypedDict
from .tools import search_tools
import google.generativeai as genai
import os

# RAG 모듈 import
try:
    from .rag.retriever import get_retriever
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("RAG 모듈을 로드할 수 없습니다. 기본 검색을 사용합니다.")


class AgentState(TypedDict):
    """Agent 상태 타입"""
    question: str
    search_results: list
    answer: str
    session_id: str
    rag_context: str  # RAG 컨텍스트 추가


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
    """정보 검색 노드 (RAG 적용)"""
    question = state.get("question", "")
    results = []
    rag_context = ""

    # RAG 검색 시도
    if RAG_AVAILABLE:
        try:
            retriever = get_retriever()
            rag_results = retriever.retrieve(question, top_k=3)

            if rag_results:
                # RAG 결과를 컨텍스트로 변환
                rag_context = retriever.retrieve_with_context(question, top_k=3)

                for r in rag_results:
                    results.append({
                        "keyword": r.get("metadata", {}).get("source", "문서"),
                        "info": r.get("content", ""),
                        "source": "rag"
                    })
        except Exception as e:
            print(f"RAG 검색 오류: {e}")

    # RAG 결과가 없으면 기본 지식 베이스 사용
    if not results:
        knowledge_base = {
            "전입신고": "전입신고는 이사 후 14일 이내에 하셔야 합니다. 주민센터 방문 또는 정부24 온라인으로 신청 가능합니다.",
            "이삿짐": "이삿짐 센터는 최소 1주일 전에 예약하시는 것이 좋습니다. 주말이나 월말에는 더 일찍 예약해야 합니다.",
            "공공요금": "이사 전에 전기, 가스, 수도 요금을 정산하고 해지 신청을 해야 합니다.",
            "인터넷": "인터넷과 TV는 이사 2주 전에 해지 또는 이전 신청을 하는 것이 좋습니다."
        }

        for keyword, info in knowledge_base.items():
            if keyword in question:
                results.append({"keyword": keyword, "info": info, "source": "fallback"})

        if not results:
            results.append({
                "keyword": "기본",
                "info": "이사 관련 정보는 정부24 또는 주민센터에 문의하시면 자세히 안내받으실 수 있습니다.",
                "source": "fallback"
            })

    return {
        **state,
        "search_results": results,
        "rag_context": rag_context
    }


async def answer_generation_node(state: AgentState) -> AgentState:
    """응답 생성 노드 (Gemini AI + RAG 사용)"""
    question = state.get("question", "")
    search_results = state.get("search_results", [])
    rag_context = state.get("rag_context", "")

    # Gemini API 설정
    api_key = os.getenv("GEMINI_API_KEY", "")

    # API 키가 있고 유효한 경우 Gemini 사용
    if api_key and api_key != "dummy_gemini_api_key" and len(api_key) > 20:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # RAG 컨텍스트가 있으면 사용, 없으면 기존 search_results 사용
            if rag_context:
                context = rag_context
            elif search_results:
                context = "\n".join([f"- {r.get('info', '')}" for r in search_results])
            else:
                context = ""

            prompt = f"""당신은 1인 가구 이사를 도와주는 친절한 AI 어시스턴트 '룸무브'입니다.

아래의 참고 문서를 기반으로 사용자의 질문에 정확하고 친절하게 답변해주세요.

=== 사용자 질문 ===
{question}

=== 참고 문서 ===
{context if context else '관련 문서가 없습니다.'}

=== 답변 지침 ===
1. 참고 문서의 내용을 기반으로 정확하게 답변하세요.
2. 친근하고 이해하기 쉬운 말투로 답변하세요.
3. 구체적인 절차나 주의사항이 있다면 포함하세요.
4. 답변은 3-5문장으로 간결하게 작성하세요.
5. 참고 문서에 없는 내용은 추측하지 말고, 일반적인 안내를 제공하세요.

답변:"""

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
