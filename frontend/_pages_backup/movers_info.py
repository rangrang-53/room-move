import streamlit as st
import pandas as pd
from utils.api_client import api_client


def render_movers_page(selected_region):
    """이삿짐 정보 페이지 렌더링"""

    st.title("🚚 이삿짐 센터 정보")

    # 필터 섹션
    st.subheader("필터")
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        # 지역 선택
        regions = [
            "전체",
            "서울 강남구",
            "서울 송파구",
            "서울 마포구",
            "서울 강서구",
            "서울 영등포구"
        ]
        filter_region = st.selectbox(
            "지역",
            regions,
            index=regions.index(selected_region) if selected_region in regions else 0
        )

    with col2:
        # 정렬 기준
        sort_by = st.selectbox(
            "정렬",
            ["가격 낮은 순", "가격 높은 순", "업체명 순"]
        )

    with col3:
        # 검색 버튼
        search_clicked = st.button("🔍 검색", use_container_width=True)

    st.markdown("---")

    # 이삿짐 센터 조회
    region_param = None if filter_region == "전체" else filter_region
    response = api_client.get_movers(region_param)

    if "error" in response:
        st.error(f"❌ 이삿짐 센터 정보를 불러올 수 없습니다: {response['error']}")
        return

    movers = response.get("movers", [])

    if not movers:
        st.info("이삿짐 센터 정보가 없습니다.")
        return

    # 데이터프레임 생성
    df = pd.DataFrame(movers)

    # 정렬
    if sort_by == "가격 낮은 순":
        df = df.sort_values("price", ascending=True)
    elif sort_by == "가격 높은 순":
        df = df.sort_values("price", ascending=False)
    elif sort_by == "업체명 순":
        df = df.sort_values("name", ascending=True)

    # 업체 카드 표시
    st.subheader(f"검색 결과 ({len(df)}개 업체)")

    for idx, row in df.iterrows():
        # 가격에 따라 색상 결정
        if row["price"] < 280000:
            price_color = "#4CAF50"  # 녹색 (저렴)
        elif row["price"] < 320000:
            price_color = "#FF9800"  # 주황색 (보통)
        else:
            price_color = "#F44336"  # 빨간색 (비쌈)

        # 카드 스타일
        st.markdown(
            f"""
            <div style="
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0 0 0.5rem 0;">{row['name']}</h3>
                <p style="margin: 0.25rem 0; color: #666;">
                    📞 {row['phone']}
                </p>
                <p style="margin: 0.25rem 0; color: #666;">
                    📍 {row['region']}
                </p>
                <div style="
                    margin-top: 1rem;
                    padding: 0.5rem 1rem;
                    background-color: {price_color};
                    color: white;
                    border-radius: 5px;
                    display: inline-block;
                    font-weight: bold;
                    font-size: 1.2rem;
                ">
                    {row['price']:,}원
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 가격 통계
    st.markdown("---")
    st.subheader("📊 가격 분석")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("최저가", f"{df['price'].min():,}원")

    with col2:
        st.metric("평균가", f"{int(df['price'].mean()):,}원")

    with col3:
        st.metric("최고가", f"{df['price'].max():,}원")
