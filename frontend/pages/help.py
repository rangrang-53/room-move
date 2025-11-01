import streamlit as st
from components.chatbot import render_chatbot


def render_help_page():
    """도움말 페이지 렌더링"""

    st.title("💬 이사 도움말")

    # 챗봇 렌더링
    render_chatbot()

    # 하단 FAQ
    st.markdown("---")
    st.subheader("📚 자주 묻는 질문 (FAQ)")

    with st.expander("❓ 전입신고는 언제 해야 하나요?"):
        st.markdown("""
        전입신고는 **이사 후 14일 이내**에 하셔야 합니다.

        **신청 방법:**
        - 주민센터 방문
        - 정부24 온라인 신청 (www.gov.kr)

        **필요 서류:**
        - 신분증
        - 임대차 계약서
        """)

    with st.expander("❓ 이삿짐 센터는 언제 예약하나요?"):
        st.markdown("""
        이삿짐 센터는 **최소 1주일 전**에 예약하시는 것이 좋습니다.

        **주의사항:**
        - 주말이나 월말에는 더 일찍 예약 필요
        - 여러 업체 견적 비교 권장
        - 보험 가입 여부 확인
        """)

    with st.expander("❓ 공공요금은 어떻게 정산하나요?"):
        st.markdown("""
        **정산 절차:**
        1. 전기, 가스, 수도 요금 최종 고지서 확인
        2. 각 회사에 해지 신청
        3. 잔여 요금 납부

        **주의사항:**
        - 이사 2~3일 전에 신청
        - 자동이체 해지 확인
        """)

    with st.expander("❓ 인터넷/TV는 언제 해지하나요?"):
        st.markdown("""
        인터넷과 TV는 **이사 2주 전**에 해지 또는 이전 신청을 하는 것이 좋습니다.

        **옵션:**
        - 해지: 완전히 끊기
        - 이전: 새 집으로 옮기기

        **주의사항:**
        - 위약금 발생 여부 확인
        - 설치 기사 방문 일정 조율
        """)

    with st.expander("❓ 우편물은 어떻게 처리하나요?"):
        st.markdown("""
        **우편물 전달 서비스:**
        - 우체국 방문 또는 인터넷우체국에서 신청
        - 최대 1년간 새 주소로 전달

        **온라인 신청:**
        - 인터넷우체국 (www.epost.go.kr)
        - 우정사업본부 앱
        """)
