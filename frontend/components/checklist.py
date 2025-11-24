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

    # 체크리스트를 하나의 컨테이너에 표시
    with st.container():
        # CSS로 간격 조정
        st.markdown("""
        <style>
        .checklist-item {
            padding: 0.3rem 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .checklist-item:last-child {
            border-bottom: none;
        }
        </style>
        """, unsafe_allow_html=True)

        for idx, item in enumerate(checklist_items):
            col1, col2 = st.columns([0.08, 0.92])

            with col1:
                # 체크박스
                checked = st.checkbox(
                    "",
                    value=item.get("completed", False),
                    key=f"check_{item['id']}",
                    label_visibility="collapsed"
                )

                # 상태 변경 시 API 호출
                if checked != item.get("completed", False):
                    update_response = api_client.update_checklist_item(
                        item["id"],
                        checked
                    )
                    if "error" not in update_response:
                        st.rerun()

            with col2:
                # 제목과 설명 (간격 줄이기) - 체크박스 현재 상태 기준으로 표시
                if checked:
                    st.markdown(f'<div style="margin-bottom: -0.5rem;"><s>{item["title"]}</s></div>', unsafe_allow_html=True)
                    if item.get("description"):
                        st.caption(f"~~{item['description']}~~")
                else:
                    st.markdown(f'<div style="margin-bottom: -0.5rem;"><strong>{item["title"]}</strong></div>', unsafe_allow_html=True)
                    if item.get("description"):
                        st.caption(item["description"])

            # 마지막 항목이 아니면 얇은 구분선
            if idx < len(checklist_items) - 1:
                st.markdown('<hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #e0e0e0;">', unsafe_allow_html=True)

        # 진행률 표시
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        completed_count = sum(1 for item in checklist_items if item.get("completed", False))
        total_count = len(checklist_items)
        progress = completed_count / total_count if total_count > 0 else 0

        st.progress(progress)
        st.caption(f"완료: {completed_count}/{total_count} ({int(progress * 100)}%)")
