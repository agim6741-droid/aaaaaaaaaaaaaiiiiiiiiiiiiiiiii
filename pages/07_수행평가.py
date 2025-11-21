import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # 상단 메타데이터 제거 (네이버 데이터랩 형식 대응)
    dessert_df = pd.read_csv("DESSERT TREND.csv", encoding="cp949", skiprows=3)
    cafe_df = pd.read_csv("CAFE.csv", encoding="cp949")

    dessert_df = dessert_df.rename(columns={dessert_df.columns[0]: "date"})
    dessert_df["date"] = pd.to_datetime(dessert_df["date"], errors="coerce")

    return dessert_df, cafe_df

dessert_df, cafe_df = load_data()

