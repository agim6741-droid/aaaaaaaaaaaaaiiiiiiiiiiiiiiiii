import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------
# 기본 설정(카페 분위기 테마)
# -----------------------
st.set_page_config(
    page_title="Dessert Trend & Cafe Recommendation",
    page_icon="🍰",
    layout="wide"
)

# CSS 스타일 커스텀 (베이지 + 브라운 톤)
st.markdown("""
    <style>
    body {
        background-color: #f5eee6;
    }
    .stApp {
        background-color: #f5eee6;
    }
    .title {
        color: #5a3e36;
        font-weight: 900;
    }
    .subtitle {
        color: #7a5448;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #c7a492;
        color: white;
        border-radius: 8px;
        height: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🍰 디저트 인기 추이 & 카페 추천 프로그램</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>선택한 기간 동안 특정 디저트의 인기도를 확인하고, 해당 디저트를 판매하는 카페를 추천받아보세요!</h4>", unsafe_allow_html=True)

# -----------------------
# 1. DESSERT.csv 분석
# -----------------------
dessert_df = pd.read_csv("/mnt/data/DESSERT.csv")

# 디저트 목록 & 기간 선택
dessert_list = sorted(dessert_df["dessert"].unique())
selected_dessert = st.selectbox("🔍 분석할 디저트를 선택하세요", dessert_list)

min_date = pd.to_datetime(dessert_df["date"]).min()
max_date = pd.to_datetime(dessert_df["date"]).max()

selected_period = st.date_input(
    "📅 기간을 선택하세요",
    [min_date, max_date]
)

# 기간 필터링
dessert_df["date"] = pd.to_datetime(dessert_df["date"])
filtered = dessert_df[
    (dessert_df["dessert"] == selected_dessert) &
    (dessert_df["date"].between(selected_period[0], selected_period[1]))
]

# -----------------------
# 4. Plotly 그래프
# -----------------------
if filtered.empty:
    st.warning("⚠️ 선택한 기간에 해당 디저트 검색 데이터가 없습니다.")
else:
    fig = px.line(
        filtered,
        x="date",
        y="search_count",
        title=f"📈 {selected_dessert} 검색량 추이",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 5. CAFE.csv 분석
# -----------------------
cafe_df = pd.read_csv("/mnt/data/CAFE.csv")

# -----------------------
# 6. 카페 추천 여부 질문
# -----------------------
st.subheader("☕ 선택한 디저트를 판매하는 카페를 추천해드릴까요?")
coffee_choice = st.radio("", ("No", "Yes"))

# -----------------------
# 7. Yes → 카페 추천
# -----------------------
if coffee_choice == "Yes":
    matching_cafe = cafe_df[cafe_df["dessert"] == selected_dessert]

    if matching_cafe.empty:
        st.error("😢 해당 디저트를 판매하는 카페 정보가 없습니다.")
    else:
        st.success(f"📍 **{selected_dessert}** 를 판매하는 카페 목록입니다!")

        for idx, row in matching_cafe.iterrows():
            st.markdown(f"""
            **🏷 카페 이름:** {row['cafe_name']}  
            **📍 위치:** {row['location']}  
            **⭐ 평점:** {row['rating']}  
            ---
            """)

else:
    st.info("추천을 원하시면 'Yes' 를 눌러주세요 ☺️")
