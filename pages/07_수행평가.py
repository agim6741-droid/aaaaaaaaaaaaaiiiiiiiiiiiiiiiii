import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dessert Trend", layout="wide")

st.markdown("## 🍰 디저트 인기 분석 & 카페 추천 프로그램")

# -----------------------------
# 1. 파일 업로드
# -----------------------------
dessert_file = st.file_uploader("📂 DESSERT.csv 파일을 업로드하세요", type=["csv"])
cafe_file = st.file_uploader("📂 CAFE.csv 파일을 업로드하세요", type=["csv"])

# 파일 없으면 STOP
if not dessert_file or not cafe_file:
    st.info("두 파일 모두 업로드하면 분석이 시작됩니다.")
    st.stop()

# -----------------------------
# 2. 판다스로 읽기
# -----------------------------
dessert_df = pd.read_csv(dessert_file)
cafe_df = pd.read_csv(cafe_file)

# 날짜 변환
dessert_df["date"] = pd.to_datetime(dessert_df["date"], errors="coerce")

# -----------------------------
# 3. 디저트 선택
# -----------------------------
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

# 필터링
filtered = dessert_df[
    (dessert_df["dessert"] == selected_dessert) &
    (dessert_df["date"].between(start_date, end_date))
]

# -----------------------------
# 4. Plotly 그래프
# -----------------------------
if filtered.empty:
    st.warning("❗ 선택한 기간에 데이터가 없습니다.")
else:
    fig = px.line(filtered, x="date", y="search_count",
                  title=f"📈 {selected_dessert} 검색량 추이",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 5. 카페 추천
# -----------------------------
st.subheader("☕ 선택한 디저트를 판매하는 카페 추천할까요?")
ask = st.radio("", ["No", "Yes"])

if ask == "Yes":
    result = cafe_df[cafe_df["dessert"] == selected_dessert]

    if result.empty:
        st.error("😢 이 디저트를 파는 카페가 없습니다.")
    else:
        st.success("📍 아래 카페를 추천드립니다!")

        for _, row in result.iterrows():
            st.markdown(f"""
            ### {row['cafe_name']}
            📍 위치: {row['location']}  
            ⭐ 평점: {row['rating']}
            ---
            """)
