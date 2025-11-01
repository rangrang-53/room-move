import streamlit as st
from utils.session_state import init_session_state
from utils.api_client import api_client
from components.sidebar import render_sidebar

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

# 사이드바 렌더링
move_date, selected_region = render_sidebar()

# 페이지 네비게이션
page = st.sidebar.radio(
    "페이지 선택",
    ["🏠 홈", "🚚 이삿짐 정보", "💬 도움말"],
    label_visibility="collapsed"
)

# 페이지 라우팅
if page == "🏠 홈":
    from pages.home import render_home_page
    render_home_page(move_date, selected_region)

elif page == "🚚 이삿짐 정보":
    from pages.movers_info import render_movers_page
    render_movers_page(selected_region)

elif page == "💬 도움말":
    from pages.help import render_help_page
    render_help_page()
