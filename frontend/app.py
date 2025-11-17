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

# ========== 우측 사이드바 ==========
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
    
    # 3. 체크리스트
    st.subheader("✅ 이사 체크리스트")
    render_checklist()
    
    st.markdown("---")
    
    # 4. 지역 선택
    st.subheader("📍 지역 선택")
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
    
    # 5. 이삿짐 정보
    with st.expander("🚚 이삿짐 업체 정보", expanded=False):
        render_movers_table(selected_region)
    
    st.markdown("---")
    
    # 앱 정보
    st.caption("**RoomMove v1.0**")
    st.caption("📧 문의: support@roommove.com")

# ========== 메인 화면 ==========
st.title("💬 AI 이사 도우미")
st.markdown("이사 준비에 대해 무엇이든 물어보세요!")

# 자주 묻는 질문 (상단 배치)
st.subheader("📚 자주 묻는 질문")

col1, col2 = st.columns(2)

with col1:
    with st.expander("❓ 전입신고는 언제 해야 하나요?"):
        st.markdown("""
        전입신고는 **이사 후 14일 이내**에 하셔야 합니다.
        
        **신청 방법:**
        - 주민센터 방문
        - 정부24 온라인 신청
        """)
    
    with st.expander("❓ 공공요금 정산은?"):
        st.markdown("""
        **정산 절차:**
        1. 전기, 가스, 수도 최종 고지서 확인
        2. 각 회사에 해지 신청
        3. 잔여 요금 납부
        """)

with col2:
    with st.expander("❓ 이삿짐 센터 예약 시기는?"):
        st.markdown("""
        이삿짐 센터는 **최소 1주일 전**에 예약하세요.
        
        **주의사항:**
        - 주말/월말은 더 일찍 예약
        - 여러 업체 견적 비교 권장
        """)
    
    with st.expander("❓ 인터넷/TV 해지는?"):
        st.markdown("""
        **이사 2주 전**에 해지 또는 이전 신청하세요.
        
        **옵션:**
        - 해지: 완전히 끊기
        - 이전: 새 집으로 옮기기
        """)

st.markdown("---")

# 챗봇 렌더링 (하단 배치)
st.subheader("💬 이사 도움말")
render_chatbot()
