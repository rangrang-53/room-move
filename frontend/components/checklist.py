import streamlit as st
from utils.api_client import api_client


def render_checklist():
    """체크리스트 컴포넌트"""

    # 체크리스트 조회
    response = api_client.get_checklist()

    # 디버깅: 응답 내용 출력
    print(f"DEBUG - Checklist response: {response}")

    if "error" in response:
        st.error(f"❌ 체크리스트를 불러올 수 없습니다: {response['error']}")
        return

    checklist_items = response.get("checklist", [])

    # 디버깅: 항목 개수 출력
    print(f"DEBUG - Checklist items count: {len(checklist_items)}")

    if not checklist_items:
        st.info("체크리스트 항목이 없습니다.")
        st.write(f"DEBUG: Response = {response}")  # 사용자에게도 보여주기
        return

    # CSS로 카드 스타일 및 간격 조정
    st.markdown("""
    <style>
    /* 완료된 항목 카드 스타일 */
    .completed-card {
        background-color: #f0f0f0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #a0a0a0;
        opacity: 0.75;
        transition: all 0.3s ease;
    }

    .completed-card:hover {
        opacity: 0.85;
    }

    /* 미완료 항목 카드 스타일 */
    .pending-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }

    .pending-card:hover {
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }

    /* 제목과 설명 간격 */
    .item-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .item-description {
        font-size: 0.85rem;
        color: #666;
        line-height: 1.5;
        margin-top: 0.5rem;
    }

    /* 체크박스 정렬 */
    [data-testid="column"]:has(input[type="checkbox"]) {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 진행률 계산
    completed_count = sum(1 for item in checklist_items if item.get("completed", False))
    total_count = len(checklist_items)
    progress = completed_count / total_count if total_count > 0 else 0

    # 진행률 바 HTML (체크리스트 위에 표시)
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            margin-bottom: 1.5rem;
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.8rem;
            ">
                <span style="font-size: 0.9rem; font-weight: 600; color: #555;">
                    📊 이사 준비 진행률
                </span>
                <span style="font-size: 1.1rem; font-weight: bold; color: #667eea;">
                    {int(progress * 100)}%
                </span>
            </div>
            <div style="
                width: 100%;
                height: 8px;
                background-color: #e0e0e0;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 0.5rem;
            ">
                <div style="
                    width: {progress * 100}%;
                    height: 100%;
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    transition: width 0.3s ease;
                "></div>
            </div>
            <div style="
                font-size: 0.85rem;
                color: #666;
                text-align: left;
            ">
                ✅ 완료: {completed_count}/{total_count} 항목
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 체크리스트 항목들
    for idx, item in enumerate(checklist_items):
        # 완료 상태에 따라 카드 스타일 결정
        is_completed = item.get("completed", False)

        # 카드 스타일 결정
        card_class = "completed-card" if is_completed else "pending-card"

        # 제목과 설명을 카드로 감싸기
        if is_completed:
            title_html = f'<div class="item-title" style="color: #888;"><s>{item["title"]}</s></div>'
            desc_html = f'<div class="item-description" style="color: #999;"><s>{item["description"]}</s></div>' if item.get("description") else ""
        else:
            title_html = f'<div class="item-title" style="color: #262730;">{item["title"]}</div>'
            desc_html = f'<div class="item-description">{item["description"]}</div>' if item.get("description") else ""

        # 카드와 체크박스를 포함한 컨테이너 (체크박스를 왼쪽에)
        col1, col2 = st.columns([0.08, 0.92])

        with col1:
            # 체크박스
            new_status = st.checkbox(
                "완료",
                value=is_completed,
                key=f"cb_{item['id']}",
                label_visibility="collapsed"
            )

            # 상태 변경 시 API 호출
            if new_status != is_completed:
                update_response = api_client.update_checklist_item(item["id"], new_status)
                if "error" not in update_response:
                    st.rerun()

        with col2:
            # 카드 HTML 렌더링
            st.markdown(
                f'<div class="{card_class}" id="card_{item["id"]}" style="margin-bottom: 0;">{title_html}{desc_html}</div>',
                unsafe_allow_html=True
            )
