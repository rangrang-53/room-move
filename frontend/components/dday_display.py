import streamlit as st
from datetime import date


def render_dday_display(move_date: date):
    """D-day 표시 컴포넌트"""
    if not move_date:
        st.warning("⚠️ 이사 날짜를 선택해주세요")
        return

    # D-day 계산
    today = date.today()
    delta = (move_date - today).days

    # 메시지 생성
    if delta > 0:
        message = f"이사까지 {delta}일 남았습니다"
        emoji = "📅"
    elif delta == 0:
        message = "오늘이 이사 날입니다!"
        emoji = "🎉"
    else:
        message = f"이사 날짜가 {abs(delta)}일 지났습니다"
        emoji = "⏰"

    # D-day 표시
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 1rem;
        ">
            <h1 style="margin: 0; font-size: 1.8rem; font-weight: bold;">D{delta:+d}</h1>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.85rem;">{message}</p>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.75rem; opacity: 0.9;">
                이사 예정일: {move_date.strftime('%Y년 %m월 %d일')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
