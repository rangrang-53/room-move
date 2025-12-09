import streamlit as st
from utils.api_client import api_client
from datetime import datetime


def render_chatbot():
    """챗봇 컴포넌트"""

    # 메신저 스타일 CSS (개선된 말풍선 + 구분선)
    st.markdown("""
    <style>
    /* 메신저 스타일 말풍선 */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        padding: 1.5rem 0;
        max-height: 500px;
        overflow-y: auto;
        background-color: #fafafa;
        border-radius: 12px;
        padding: 1.5rem;
    }

    .message-row {
        display: flex;
        margin: 0.5rem 0;
        align-items: flex-start;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .message-bubble {
        max-width: 70%;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        word-wrap: break-word;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        line-height: 1.6;
    }

    .message-bubble.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }

    .message-bubble.assistant {
        background-color: #ffffff;
        color: #262730;
        border-bottom-left-radius: 4px;
        border: 2px solid #e0e0e0;
    }

    .message-bubble p {
        margin: 0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    # 대화 이력 표시
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # 기본 환영 메시지 (예시 대화 포함)
    if len(st.session_state.chat_messages) == 0:
        st.session_state.chat_messages.extend([
            {
                "role": "assistant",
                "content": "안녕하세요! 이사 준비에 대해 궁금한 점을 물어보세요. 도와드리겠습니다."
            },
            {
                "role": "assistant",
                "content": "💡 예시: '전입신고는 언제 해야 하나요?', '이삿짐 센터는 어떻게 예약하나요?'"
            }
        ])

    # 대화 이력 렌더링 (메신저 스타일)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in st.session_state.chat_messages:
        role = message["role"]
        content = message["content"]

        # HTML로 메신저 스타일 말풍선 생성
        st.markdown(f"""
        <div class="message-row {role}">
            <div class="message-bubble {role}">
                <p>{content}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 사용자 입력 (placeholder 추가)
    user_input = st.chat_input("예: 전입신고 언제 해요?")

    # 초기화 버튼 (입력창 아래에 우측 정렬)
    if len(st.session_state.chat_messages) > 1:
        st.markdown("""
        <style>
        /* 초기화 버튼만 선택 */
        button[data-testid="baseButton-secondary"][key="reset_chat"],
        button[kind="secondary"]:has-text("🗑️ 초기화") {
            background-color: #ff6b6b !important;
            color: white !important;
            border: none !important;
            border-radius: 999px !important;
            padding: 0.4rem 1rem !important;
            font-size: 0.8rem !important;
            float: right !important;
            margin-top: -3rem !important;
            margin-right: 0.5rem !important;
            position: relative !important;
            z-index: 100 !important;
        }

        /* 초기화 버튼 호버 */
        button[kind="secondary"]:has-text("🗑️ 초기화"):hover {
            background-color: #ff5252 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("🗑️ 초기화", key="reset_chat", type="secondary"):
            st.session_state.chat_messages = []
            st.rerun()

    # 빠른 질문 버튼 클릭 처리
    quick_question = None
    if "quick_question" in st.session_state and st.session_state.quick_question:
        quick_question = st.session_state.quick_question
        st.session_state.quick_question = None  # 초기화

    # 입력이 있으면 처리 (빠른 질문 또는 직접 입력)
    prompt = quick_question if quick_question else user_input

    if prompt:
        # 사용자 메시지 추가
        st.session_state.chat_messages.append({
            "role": "user",
            "content": prompt
        })

        # 임시 로딩 메시지 추가
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "💭 답변 생성 중..."
        })

        # 페이지 새로고침으로 로딩 메시지 표시
        st.rerun()

    # 로딩 중인 메시지가 있으면 API 호출
    if (len(st.session_state.chat_messages) > 0 and
        st.session_state.chat_messages[-1]["content"] == "💭 답변 생성 중..."):

        # 사용자의 마지막 질문 찾기
        user_question = None
        for i in range(len(st.session_state.chat_messages) - 2, -1, -1):
            if st.session_state.chat_messages[i]["role"] == "user":
                user_question = st.session_state.chat_messages[i]["content"]
                break

        if user_question:
            # 자동 체크 API 호출 (메시지에서 완료된 작업 감지)
            auto_check_response = api_client.auto_check_from_message(user_question)
            has_auto_check = auto_check_response and auto_check_response.get("checked_items")

            # 챗봇 API 호출
            response = api_client.send_chat_message(user_question)

            if "error" in response:
                answer = f"죄송합니다. 오류가 발생했습니다: {response['error']}"
            else:
                answer = response.get("answer", "응답을 생성할 수 없습니다.")

            # 자동 체크 메시지가 있으면 별도 말풍선으로 먼저 표시
            if has_auto_check:
                auto_check_message = f"✅ {auto_check_response.get('message', '')}"
                # 로딩 메시지를 자동 체크 메시지로 교체
                st.session_state.chat_messages[-1]["content"] = auto_check_message
                # 챗봇 답변을 새 말풍선으로 추가
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                # 로딩 메시지를 실제 답변으로 교체
                st.session_state.chat_messages[-1]["content"] = answer

            # 페이지 새로고침으로 실제 답변 표시
            st.rerun()
