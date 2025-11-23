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

# ===== CSV 업로드 =====
st.subheader("📁 DESSERT.csv 파일을 업로드하세요")
dessert_file = st.file_uploader("DESSERT.csv", type=["csv"])

st.subheader("📁 CAFE.csv 파일을 업로드하세요")
cafe_file = st.file_uploader("CAFE.csv", type=["csv"])

# 파일 둘 다 업로드되었을 때만 실행
if dessert_file is not None and cafe_file is not None:

    dessert_df = pd.read_csv(dessert_file)
    cafe_df = pd.read_csv(cafe_file)

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

    # 텍스트 → 숫자로 변환
    filtered[selected_dessert] = pd.to_numeric(filtered[selected_dessert], errors="coerce")

    # 그래프 출력
    fig = px.line(
        filtered,
        x="날짜",
        y=selected_dessert,
        title=f"{selected_dessert} 검색량 변화",
        markers=True
    )
    st.plotly_chart(fig)

    # 카페 추천
    st.subheader("선택한 디저트를 판매하는 카페를 추천해드릴까요?")
    choice = st.radio("", ["yes", "no"], horizontal=True)

    if choice == "yes":
        cafe_match = cafe_df[cafe_df["디저트"] == selected_dessert]

        if len(cafe_match) == 0:
            st.write("😢 해당 디저트를 판매하는 카페 정보가 없습니다.")
        else:
            for idx, row in cafe_match.iterrows():
                st.write(f"### ☕ {row['카페1']} / {row['카페2']}")
                st.write(f"- 위치 : {row['위치1']}, {row['위치2']}")
                st.write(f"- 비고 : {row['비고']}")
                st.write("---")
