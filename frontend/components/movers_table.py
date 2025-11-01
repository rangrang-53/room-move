import streamlit as st
import pandas as pd
from utils.api_client import api_client


def render_movers_table(region: str = None, show_all: bool = False):
    """이삿짐 센터 테이블 컴포넌트"""

    if not show_all:
        st.subheader("🚚 이삿짐 센터 정보")

    # 이삿짐 센터 조회
    response = api_client.get_movers(region if not show_all else None)

    if "error" in response:
        st.error(f"❌ 이삿짐 센터 정보를 불러올 수 없습니다: {response['error']}")
        return

    movers = response.get("movers", [])

    if not movers:
        st.info("이삿짐 센터 정보가 없습니다.")
        return

    # 데이터프레임 생성
    df = pd.DataFrame(movers)

    # 컬럼 선택 및 이름 변경
    display_df = df[["name", "phone", "price"]].copy()
    display_df.columns = ["업체명", "연락처", "예상 금액"]

    # 가격 포맷팅
    display_df["예상 금액"] = display_df["예상 금액"].apply(
        lambda x: f"{x:,}원"
    )

    # 테이블 표시
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # 정렬 옵션
    if show_all:
        st.caption(f"총 {len(movers)}개 업체")
    else:
        st.caption(f"{region} 지역 - 총 {len(movers)}개 업체")
