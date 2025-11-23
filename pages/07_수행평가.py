import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="디저트 유행 분석", layout="wide")

# ===== 배경색 =====
page_style = """
<style>
body { background-color: #f7f1e3; }
.sidebar .sidebar-content { background-color: #d2b48c; }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

st.title("🍰 디저트 유행 분석 & 카페 추천")

# ===== CSV 파일 경로 =====
dessert_path = "DESSERT.csv"
cafe_path = "CAFE.csv"

# ===== 파일 존재 여부 체크 =====
if not os.path.exists(dessert_path) or not os.path.exists(cafe_path):
    st.error("❌ CSV 파일이 존재하지 않습니다. 앱 폴더 안에 'DESSERT.csv'와 'CAFE.csv'를 넣어주세요.")
    st.stop()

# ===== CSV 읽기 (인코딩 자동 처리) =====
def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except:
        return pd.read_csv(path, encoding="cp949")

dessert_df = read_csv_safe(dessert_path)
cafe_df = read_csv_safe(cafe_path)

# ===== 컬럼명 공백 제거 =====
dessert_df.columns = dessert_df.columns.str.strip()
cafe_df.columns = cafe_df.columns.str.strip()

# ===== 컬럼 체크 =====
required_dessert_cols = ["날짜"] + list(dessert_df.columns[1:])
if "날짜" not in dessert_df.columns or len(dessert_df.columns) < 2:
    st.error("❌ DESSERT.csv에 '날짜' 컬럼 또는 디저트 컬럼이 없습니다.")
    st.stop()

if "디저트" not in cafe_df.columns:
    st.error("❌ CAFE.csv에 '디저트' 컬럼이 없습니다.")
    st.stop()

# ===== 날짜 변환 =====
dessert_df["날짜"] = pd.to_datetime(dessert_df["날짜"], errors="coerce")

# ===== 디저트 선택 =====
dessert_list = list(dessert_df.columns[1:])
selected_dessert = st.selectbox("디저트를 선택하세요", dessert_list)

# ===== 기간 선택 =====
start_date = st.date_input("시작 날짜", value=dessert_df["날짜"].min().date())
end_date = st.date_input("종료 날짜", value=dessert_df["날짜"].max().date())

mask = (dessert_df["날짜"] >= pd.to_datetime(start_date)) & \
       (dessert_df["날짜"] <= pd.to_datetime(end_date))
filtered = dessert_df[mask].copy()
filtered[selected_dessert] = pd.to_numeric(filtered[selected_dessert], errors="coerce")

# ===== 그래프 =====
fig = px.line(
    filtered,
    x="날짜",
    y=selected_dessert,
    title=f"{selected_dessert} 검색량 변화",
    markers=True,
    line_shape='spline',
    template='plotly_white'
)
st.plotly_chart(fig)

# ===== 카페 추천 =====
st.subheader("선택한 디저트를 판매하는 카페를 추천해드릴까요?")
choice = st.radio("", ["yes", "no"], horizontal=True)

if choice == "yes":
    cafe_match = cafe_df[cafe_df["디저트"].str.strip().str.lower() == selected_dessert.lower()]

    if len(cafe_match) == 0:
        st.write("😢 해당 디저트를 판매하는 카페 정보가 없습니다.")
    else:
        for idx, row in cafe_match.iterrows():
            st.write(f"### ☕ {row.get('카페1','')} / {row.get('카페2','')}")
            st.write(f"- 위치 : {row.get('위치1','')}, {row.get('위치2','')}")
            st.write(f"- 비고 : {row.get('비고','')}")
            st.write("---")
