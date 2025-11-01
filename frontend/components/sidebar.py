import streamlit as st
from datetime import date, timedelta


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.title("🏠 RoomMove")
        st.markdown("---")

        # 이사 날짜 입력
        st.subheader("이사 날짜 입력")
        default_date = date.today() + timedelta(days=14)
        move_date = st.date_input(
            "이사 예정일",
            value=default_date,
            min_value=date.today(),
            help="이사 예정 날짜를 선택하세요"
        )
        st.session_state.move_date = move_date

        st.markdown("---")

        # 지역 선택
        st.subheader("지역 선택")
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
            help="이삿짐 센터를 검색할 지역을 선택하세요"
        )
        st.session_state.selected_region = selected_region

        st.markdown("---")

        # 앱 정보
        st.subheader("앱 정보")
        st.info("""
        **RoomMove v1.0**

        1인 가구 이사 준비 도우미

        📧 문의: support@roommove.com
        """)

    return move_date, selected_region
