import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------------------------
# 기본 설정
# ---------------------------------------------
st.set_page_config(
    page_title="Dessert Trend",
    page_icon="🍰",
    layout="wide"
)

# ---------------------------------------------
# 1. CSV를 앱 내부에서 불러오기 (상대경로)
# ---------------------------------------------
try:
    dessert_df = pd.read_csv("DESSERT.csv")
    cafe_df = pd.read_csv("CAFE.csv")
except FileNotFoundError:
    st.error("❌ csv 파일이 앱 폴더에 없습니다. DESSERT.csv, CAFE.csv 두 파일을 app.py와 같은 폴더에 넣어주세요!")
    st.stop()

# 날짜 변환
dessert_df["date"] = pd.to_datetime(dessert_df["date"], errors="coerce")

st.markdown("## 🍰 디저트 인기 분석 & 카페 추천 프로그램")

# ---------------------------------------------
# 2. 디저트 선택
# ---------------------------------------------
dessert_list = sorted(dessert_df["dessert"].unique())
selected_dessert = st.selectbox("🔍 분석할 디저트 선택", dessert_list)

# 기간 선택
min_date = dessert_df["date"].min()
max_date = dessert_df["date"].max()

start_date, end_date = st.date_input(
    "📅 조회 기간 선택",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 기간 필터링
filtered = dessert_df[
    (dessert_df["dessert"] == selected_dessert) &
    (dessert_df["date"].between(start_date, end_date))
]

# ---------------------------------------------
# 3. Plotly 그래프
# ---------------------------------------------
if filtered.empty:
    st.warning("⚠️ 선택한 기간에 데이터가 없습니다.")
else:
    fig = px.line(
        filtered,
        x="date",
        y="search_count",
        title=f"📈 {selected_dessert} 검색량 추이",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------
# 4. 카페 추천
# ---------------------------------------------
st.subheader("☕ 선택한 디저트를 판매하는 카페 추천할까요?")
ask = st.radio("", ["No", "Yes"])

if ask == "Yes":
    result = cafe_df[cafe_df["dessert"] == selected_dessert]

    if result.empty:
        st.error("😢 이 디저트를 파는 카페가 없습니다.")
    else:
        st.success(f"📍 {selected_dessert}을 판매하는 카페 목록입니다!")

        for _, row in result.iterrows():
            st.markdown(f"""
            ### {row['cafe_name']}
            📍 위치: {row['location']}  
            ⭐ 평점: {row['rating']}
            ---
            """)
else:
    st.info("추천을 원하면 'Yes'를 눌러줘 😊")
