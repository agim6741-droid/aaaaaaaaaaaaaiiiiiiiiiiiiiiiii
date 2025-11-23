import streamlit as st
import pandas as pd
import plotly.express as px

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

# ===== CSV 파일 불러오기 =====
dessert_df = pd.read_csv("DESSERT.csv", encoding="utf-8-sig")
cafe_df = pd.read_csv("CAFE.csv", encoding="utf-8-sig")

# 날짜 변환
dessert_df["날짜"] = pd.to_datetime(dessert_df["날짜"], errors="coerce")

# 디저트 리스트
dessert_list = list(dessert_df.columns[1:])
selected_dessert = st.selectbox("디저트를 선택하세요", dessert_list)

# 기간 선택
start_date = st.date_input("시작 날짜", value=dessert_df["날짜"].min().date())
end_date = st.date_input("종료 날짜", value=dessert_d_
