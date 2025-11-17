import streamlit as st
from components.dday_display import render_dday_display
from components.checklist import render_checklist
from components.movers_table import render_movers_table


def render_home_page(move_date, selected_region):
    """홈 페이지 렌더링"""

    st.title("🏠 이사 준비 대시보드")

    # D-day 표시
    render_dday_display(move_date)

    # 2단 레이아웃
    col1, col2 = st.columns([1, 1])

    with col1:
        # 체크리스트
        render_checklist()

    with col2:
        # 이삿짐 센터 정보 (선택된 지역)
        render_movers_table(selected_region, show_all=False)

    # 하단 안내
    st.markdown("---")
    st.info("""
    💡 **사용 팁**
    - 왼쪽 사이드바에서 이사 날짜와 지역을 설정하세요
    - 체크리스트를 확인하며 이사 준비를 진행하세요
    - 🚚 이삿짐 정보 페이지에서 더 많은 업체를 비교할 수 있습니다
    - 💬 도움말 페이지에서 이사 관련 질문을 할 수 있습니다
    """)
