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

    # D-day 형식 결정 (양수: -, 0: Day, 음수: +)
    if delta > 0:
        dday_text = f"D-{delta}"
    elif delta == 0:
        dday_text = "D-Day"
    else:
        dday_text = f"D+{abs(delta)}"

    # D-day 표시 (톤 다운 + 아이콘 추가)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            padding: 1.2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
            <h1 style="margin: 0; font-size: 2rem; font-weight: bold; color: #667eea;">{dday_text}</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #555; font-weight: 500;">{message}</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #888;">
                {move_date.strftime('%Y년 %m월 %d일')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
