import pytest
from agent.graph import agent
from agent.nodes import question_understanding_node, search_node, answer_generation_node


@pytest.mark.asyncio
async def test_agent_run():
    """Agent 실행 테스트"""
    result = await agent.run("전입신고는 언제 하나요?", "test-session")

    assert "question" in result
    assert "answer" in result
    assert "session_id" in result
    assert len(result["answer"]) > 0


@pytest.mark.asyncio
async def test_question_understanding_node():
    """질문 이해 노드 테스트"""
    state = {
        "question": "  전입신고는 언제?  ",
        "search_results": [],
        "answer": "",
        "session_id": "test"
    }

    result = await question_understanding_node(state)

    assert result["question"] == "전입신고는 언제?"


@pytest.mark.asyncio
async def test_search_node_with_keyword():
    """키워드 매칭 검색 노드 테스트"""
    state = {
        "question": "전입신고 언제 하나요?",
        "search_results": [],
        "answer": "",
        "session_id": "test"
    }

    result = await search_node(state)

    assert len(result["search_results"]) > 0
    assert "전입신고" in result["search_results"][0]["keyword"]


@pytest.mark.asyncio
async def test_search_node_without_keyword():
    """키워드 없는 검색 노드 테스트"""
    state = {
        "question": "안녕하세요",
        "search_results": [],
        "answer": "",
        "session_id": "test"
    }

    result = await search_node(state)

    # 기본 응답이 있어야 함
    assert len(result["search_results"]) > 0


@pytest.mark.asyncio
async def test_answer_generation_node():
    """응답 생성 노드 테스트"""
    state = {
        "question": "전입신고는 언제?",
        "search_results": [
            {
                "keyword": "전입신고",
                "info": "전입신고는 이사 후 14일 이내에 하셔야 합니다."
            }
        ],
        "answer": "",
        "session_id": "test"
    }

    result = await answer_generation_node(state)

    assert len(result["answer"]) > 0
    assert "14일" in result["answer"]
