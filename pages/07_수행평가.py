import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------- 데이터 로드 ----------------------
@st.cache_data
def load_data():
    dessert_df = pd.read_csv("DESSERT TREND.csv", encoding="cp949")
    cafe_df = pd.read_csv("CAFE.csv", encoding="cp949")

    # 전처리: 상단 불필요 행 제거 & 날짜 변환
    dessert_df = dessert_df.rename(columns={dessert_df.columns[0]: "date"})
    dessert_df["date"] = pd.to_datetime(dessert_df["date"])

    return dessert_df, cafe_df

dessert_df, cafe_df = load_data()

# ---------------------- UI 제목 ----------------------
st.title("🍰 2023.11 ~ 2025.11 디저트 트렌드 분석 Dashboard")
st.write("네이버 데이터랩 활용 · 실시간 디저트 인기 변화 확인")

# ---------------------- 선택 옵션 ----------------------
desserts = list(dessert_df.columns[1:])  # 첫 열은 날짜
selected_dessert = st.selectbox("📍 분석할 디저트를 선택하세요", desserts)

# 기간 선택
start_date = st.date_input("시작 날짜 선택", value=dessert_df["date"].min())
end_date = st.date_input("종료 날짜 선택", value=dessert_df["date"].max())

# ---------------------- 필터링 ----------------------
filtered = dessert_df[(dessert_df["date"] >= pd.to_datetime(start_date)) &
                      (dessert_df["date"] <= pd.to_datetime(end_date))]

# ---------------------- 그래프 ----------------------
st.subheader(f"📈 {selected_dessert} 검색량 추이")
fig = px.line(filtered, x="date", y=selected_dessert)
fig.update_layout(xaxis_title="날짜", yaxis_title="검색량", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ---------------------- 추천 카페 안내 ----------------------
st.write(" ")
st.subheader("☕ 추천 카페 안내 기능")
recommend = st.radio("선택한 디저트를 판매하는 카페 추천을 보시겠습니까?", ["No", "Yes"])

if recommend == "Yes":
    st.success(f"'{selected_dessert}' 판매 카페 추천 결과 📍")

    selected_row = cafe_df[cafe_df["디저트"] == selected_dessert]

    if not selected_row.empty:
        cafe1 = selected_row.iloc[0]["카페1"]
        cafe2 = selected_row.iloc[0]["카페2"]
        loc1 = selected_row.iloc[0]["위치1"]
        loc2 = selected_row.iloc[0]["위치2"]
        desc = selected_row.iloc[0]["비고"]

        st.write(f"✨ **{cafe1}** — 위치: {loc1}")
        st.write(f"✨ **{cafe2}** — 위치: {loc2}")
        st.write(f"📝 비고: {desc}")
    else:
        st.error("해당 디저트를 판매하는 카페 데이터가 없습니다 😢")
else:
    st.info("카페 추천을 보시려면 'Yes'를 선택하세요 ☺️")
