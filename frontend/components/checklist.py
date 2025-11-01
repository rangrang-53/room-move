import streamlit as st
from utils.api_client import api_client


def render_checklist():
    """체크리스트 컴포넌트"""
    st.subheader("📋 체크리스트")

    # 체크리스트 조회
    response = api_client.get_checklist()

    if "error" in response:
        st.error(f"❌ 체크리스트를 불러올 수 없습니다: {response['error']}")
        return

    checklist_items = response.get("checklist", [])

    if not checklist_items:
        st.info("체크리스트 항목이 없습니다.")
        return

    # 체크리스트 표시
    for item in checklist_items:
        col1, col2 = st.columns([0.1, 0.9])

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
            # 제목과 설명
            if item.get("completed", False):
                st.markdown(f"~~{item['title']}~~")
                if item.get("description"):
                    st.caption(f"~~{item['description']}~~")
            else:
                st.markdown(f"**{item['title']}**")
                if item.get("description"):
                    st.caption(item["description"])

        st.markdown("---")

    # 진행률 표시
    completed_count = sum(1 for item in checklist_items if item.get("completed", False))
    total_count = len(checklist_items)
    progress = completed_count / total_count if total_count > 0 else 0

    st.progress(progress)
    st.caption(f"완료: {completed_count}/{total_count} ({int(progress * 100)}%)")
