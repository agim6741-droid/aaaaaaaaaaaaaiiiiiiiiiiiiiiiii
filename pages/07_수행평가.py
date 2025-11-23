import streamlit as st
import pandas as pd
import plotly.express as px

# ==== 페이지 스타일 ====
st.set_page_config(page_title="디저트 유행 분석", layout="wide")

page_style = """
<style>
body {
    background-color: #f7f1e3; /* 베이지 */
}
.sidebar .sidebar-content {
    background-color: #d2b48c; /* 브라운 */
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# ==== CSV 불러오기 ====
dessert_df = pd.read_csv("/mnt/data/DESSERT.csv")
cafe_df = pd.read_csv("/mnt/data/CAFE.csv")

# 날짜 컬럼 변환
dessert_df["날짜"] = pd.to_datetime(dessert_df["날짜"], errors="coerce")

# ==== 제목 ====
st.title("🍰 디저트 유행 분석 & 카페 추천")

# ==== 디저트 선택 ====
dessert_list = list(dessert_df.columns[1:])   # 첫 컬럼 '날짜' 제외
selected_dessert = st.selectbox("디저트를 선택하세요", dessert_list)

# ==== 기간 선택 ====
start_date = st.date_input("시작 날짜", value=dessert_df["날짜"].min().date())
end_date = st.date_input("종료 날짜", value=dessert_df["날짜"].max().date())

# ==== 필터링 ====
mask = (dessert_df["날짜"] >= pd.to_datetime(start_date)) & \
       (dessert_df["날짜"] <= pd.to_datetime(end_date))
filtered = dessert_df[mask].copy()

# 검색량이 텍스트라서 숫자로 변환
filtered[selected_dessert] = pd.to_numeric(filtered[selected_dessert], errors="coerce")

# ==== 그래프 출력 ====
fig = px.line(
    filtered,
    x="날짜",
    y=selected_dessert,
    title=f"{selected_dessert} 검색량 변화",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# ==== 카페 추천 여부 ====
st.subheader("선택한 디저트를 판매하는 카페를 추천해드릴까요?")
choice = st.radio("", ["yes", "no"], horizontal=True)

if choice == "yes":
    st.write("📍 **추천 카페 목록**")

    cafe_match = cafe_df[cafe_df["디저트"] == selected_dessert]

    if len(cafe_match) == 0:
        st.write("😢 해당 디저트를 판매하는 카페 정보가 없습니다.")
    else:
        for idx, row in cafe_match.iterrows():
            st.write(f"### ☕ {row['카페1']} / {row['카페2']}")
            st.write(f"- 위치 : {row['위치1']}, {row['위치2']}")
            st.write(f"- 비고 : {row['비고']}")
            st.write("---")
else:
    st.write("카페 추천을 종료합니다 😊")
