import streamlit as st
from utils.api_client import api_client
from datetime import datetime


def render_chatbot():
    """챗봇 컴포넌트"""

    st.subheader("💬 이사 도움말")

    # 챗봇 안내
    with st.expander("ℹ️ 사용 방법", expanded=False):
        st.markdown("""
        **이사 관련 질문을 자유롭게 해보세요!**

        예시 질문:
        - 전입신고는 언제 해야 하나요?
        - 이삿짐 센터는 언제 예약하나요?
        - 공공요금 해지는 어떻게 하나요?
        - 인터넷 해지 신청은 언제 하나요?
        """)

    # 대화 이력 표시
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # 기본 환영 메시지
    if len(st.session_state.chat_messages) == 0:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "안녕하세요! 이사 준비에 대해 궁금한 점을 물어보세요. 도와드리겠습니다."
        })

    # 대화 이력 렌더링
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.chat_messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # API 호출
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                response = api_client.send_chat_message(prompt)

                if "error" in response:
                    answer = f"죄송합니다. 오류가 발생했습니다: {response['error']}"
                else:
                    answer = response.get("answer", "응답을 생성할 수 없습니다.")

                st.markdown(answer)

                # 어시스턴트 메시지 추가
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })

    # 대화 초기화 버튼
    if len(st.session_state.chat_messages) > 1:
        if st.button("🗑️ 대화 초기화"):
            st.session_state.chat_messages = []
            st.rerun()
