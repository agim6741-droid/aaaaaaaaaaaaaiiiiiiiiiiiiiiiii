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

# ===== CSV 파일 존재 여부 체크 =====
if not os.path.exists(dessert_path):
    st.error(f"❌ {dessert_path} 파일을 찾을 수 없습니다. 경로를 확인하세요.")
elif not os.path.exists(cafe_path):
    st.error(f"❌ {cafe_path} 파일을 찾을 수 없습니다. 경로를 확인하세요.")
else:
    # ===== CSV 불러오기 =====
    try:
        dessert_df = pd.read_csv(dessert_path, encoding="utf-8-sig")
    except:
        dessert_df = pd.read_csv(dessert_path, encoding="cp949")  # 윈도우용

    try:
        cafe_df = pd.read_csv(cafe_path, encoding="utf-8-sig")
    except:
        cafe_df = pd.read_csv(cafe_path, encoding="cp949")

    # ===== 컬럼 체크 =====
    if "날짜" not in dessert_df.columns:
        st.error("❌ DESSERT.csv에 '날짜' 컬럼이 없습니다.")
    elif len(dessert_df.columns) < 2:
        st.error("❌ DESSERT.csv에 디저트 컬럼이 없습니다.")
    elif "디저트" not in cafe_df.columns:
        st.error("❌ CAFE.csv에 '디저트' 컬럼이 없습니다.")
    else:
        # 날짜 변환
        dessert_df["날짜"] = pd.to_datetime(dessert_df["날짜"], errors="coerce")

        # 디저트 리스트
        dessert_list = list(dessert_df.columns[1:])
        selected_dessert = st.selectbox("디저트를 선택하세요", dessert_list)

        # 기간 선택
        start_date = st.date_input("시작 날짜", value=dessert_df["날짜"].min().date())
        end_date = st.date_input("종료 날짜", value=dessert_df["날짜"].max().date())

        mask = (dessert_df["날짜"] >= pd.to_datetime(start_date)) & \
               (dessert_df["날짜"] <= pd.to_datetime(end_date))
        filtered = dessert_df[mask].copy()
        filtered[selected_dessert] = pd.to_numeric(filtered[selected_dessert], errors="coerce")

        # 그래프 출력
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

        # 카페 추천
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
