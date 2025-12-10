import streamlit as st
from datetime import date, timedelta
from utils.session_state import init_session_state
from utils.api_client import api_client
from components.chatbot import render_chatbot
from components.dday_display import render_dday_display
from components.checklist import render_checklist
from components.movers_table import render_movers_table

# 페이지 설정
st.set_page_config(
    page_title="RoomMove - 이사 준비 도우미",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
init_session_state()

# API 클라이언트 세션 ID 설정
api_client.set_session_id(st.session_state.session_id)


# ========== 좌측 사이드바 ==========
with st.sidebar:
    st.title("🏠 RoomMove")
    st.markdown("*1인 가구 이사 준비 도우미*")
    st.markdown("---")

    # 1. 이사 날짜 입력
    st.subheader("📅 이사 날짜 입력")
    default_date = date.today() + timedelta(days=14)
    move_date = st.date_input(
        "이사 예정일",
        value=default_date,
        min_value=date.today(),
        help="이사 예정 날짜를 선택하세요",
        label_visibility="collapsed"
    )
    st.session_state.move_date = move_date

    # 2. D-DAY 표시
    render_dday_display(move_date)

    st.markdown("---")

    # 3. 지역 선택
    st.subheader("📍 지역 선택")
    st.caption("이삿짐 센터를 검색할 지역을 선택하세요")
    regions = [
        "서울 강남구",
        "서울 송파구",
        "서울 마포구",
        "서울 강서구",
        "서울 영등포구"
    ]
    selected_region = st.selectbox(
        "이삿짐 센터 지역",
        regions,
        index=0,
        help="이삿짐 센터를 검색할 지역을 선택하세요",
        label_visibility="collapsed"
    )
    st.session_state.selected_region = selected_region

    # 지역 정보 요약 표시
    st.markdown(
        f"""
        <div style="
            background-color: rgba(102, 126, 234, 0.1);
            padding: 0.8rem;
            border-radius: 8px;
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: #555;
        ">
            📌 선택된 지역: <strong>{selected_region}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. 이삿짐 정보
    with st.expander("🚚 이삿짐 업체 정보", expanded=False):
        render_movers_table(selected_region)

    st.markdown("---")

    # 앱 정보
    st.caption("**RoomMove v1.0**")
    st.caption("📧 문의: support@roommove.com")

# ========== 메인 화면 및 우측 사이드바 ==========
# 메인 화면과 우측 사이드바를 컬럼으로 분할 (비율 조정: 왼쪽 축소, 오른쪽 확대)
col_main, col_right = st.columns([2.5, 1.5])

# 빠른 질문 버튼 스타일링
st.markdown("""
<style>
/* 빠른 질문 버튼 스타일 */
.stButton > button {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
    color: #667eea !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.2rem !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%) !important;
    border: 2px solid rgba(102, 126, 234, 0.4) !important;
}

.stButton > button:active {
    transform: none !important;
}

</style>
""", unsafe_allow_html=True)

with col_main:
    # 챗봇 중심 UI
    st.title("💬 AI 이사 도우미")

    # 빠른 질문 버튼들 (채팅 UI 느낌)
    st.markdown("##### 💡 빠른 질문")
    quick_q1, quick_q2, quick_q3, quick_q4 = st.columns(4)

    with quick_q1:
        if st.button("📝 전입신고", use_container_width=True):
            st.session_state.quick_question = "전입신고는 언제 해야 하나요?"

    with quick_q2:
        if st.button("💰 공공요금", use_container_width=True):
            st.session_state.quick_question = "공공요금은 어떻게 정산하나요?"

    with quick_q3:
        if st.button("🚚 이삿짐", use_container_width=True):
            st.session_state.quick_question = "이삿짐 센터는 언제 예약하나요?"

    with quick_q4:
        if st.button("📡 인터넷", use_container_width=True):
            st.session_state.quick_question = "인터넷/TV는 어떻게 해지하나요?"

    st.markdown("---")

    # 챗봇 렌더링 (메인)
    render_chatbot()

with col_right:
    st.markdown('<h3 style="margin-top: 0; padding-top: 0;">✅ 이사 체크리스트</h3>', unsafe_allow_html=True)
    render_checklist()
