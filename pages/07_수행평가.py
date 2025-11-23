import pandas as pd
import streamlit as st
import plotly.express as px
import re

st.set_page_config(page_title="Dessert Trend", page_icon="🍰", layout="wide")

# -------------------------------------------------
# 1. CSV 불러오기 (앱 폴더 안에 넣어두기!)
# -------------------------------------------------
dessert_df = pd.read_csv("DESSERT.csv")
cafe_df = pd.read_csv("CAFE.csv")

# -------------------------------------------------
# 2. DESSERT.csv 전처리 (Wide → Long)
# -------------------------------------------------
# 숫자만 추출하는 함수 (텍스트 → 숫자)
def extract_number(x):
    if pd.isna(x):
        return None
    num = re.findall(r"\d+", str(x))
    return int(num[0]) if num else None

# Long 형태로 변환
dessert_df = pd.melt(
    dessert_df,
    id_vars=["날짜"],
    var_name="dessert",
    value_name="search_count"
)

# 날짜, 검색량 가공
dessert_df.rename(columns={"날짜": "date"}, inplace=True)
dessert_df["date"] = pd.to_datetime(dessert_df["date"], errors="coerce")
dessert_df["search_count"] = dessert_df["search_count"].apply(extract_number)

# -------------------------------------------------
# 3. CAFE.csv 전처리 (카페1/2 → 개별 행으로 분리)
# -------------------------------------------------
rows = []

for _, row in cafe_df.iterrows():
    if pd.notna(row["카페1"]):
       
