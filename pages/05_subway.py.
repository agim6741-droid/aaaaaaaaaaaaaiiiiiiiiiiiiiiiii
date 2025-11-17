import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Subway Top10 OCT 2025", layout="wide")
st.title("🚇 지하철 승하차 Top10 분석")

uploaded = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded is None:
    st.info("⬆️ CSV 파일을 왼쪽에서 업로드해주세요")
    st.stop()

@st.cache_data(ttl=600)
def load_data(file):
    encodings = ["utf-8", "cp949"]
    for e in encodings:
        try:
            return pd.read_csv(file, encoding=e)
        except:
            pass
    st.error("❌ 파일 인코딩을 읽을 수 없습니다.")
    st.stop()

df = load_data(uploaded)

st.sidebar.subheader("✔ 컬럼 확인")
st.sidebar.write(list(df.columns))

# 컬럼 자동 매핑
col_date = [c for c in df.columns if "사용일" in c][0]
col_line = [c for c in df.columns if "노선" in c][0]
col_station = [c for c in df.columns if "역" in c][0]
col_on = [c for c in df.columns if "승차" in c][0]
col_off = [c for c in df.columns if "하차" in c][0]

df[col_date] = pd.to_datetime(df[col_date].astype(str), errors="coerce")
df["승하합계"] = df[col_on] + df[col_off]

date_sel = st.sidebar.date_input("날짜 선택", df[col_date].min())
line_sel = st.sidebar.selectbox("호선 선택", sorted(df[col_line].unique()))

filtered = df[(df[col_date].dt.date == date_sel) & (df[col_line] == line_sel)]

if filtered.empty:
    st.error("❌ 해당 조건에 데이터 없음")
    st.stop()

top10 = filtered.groupby(col_station, as_index=False)["승하합계"].sum().sort_values("승하합계", ascending=False).head(10)
top10["rank"] = top10.index + 1

burgundy = "rgba(128,0,32,1)"
baby = (255, 182, 193)
opacities = np.linspace(1.0, 0.3, len(top10))
colors = [burgundy if i==0 else f"rgba({baby[0]},{baby[1]},{baby[2]},{opacities[i]:.3f})" for i in range(len(top10))]

fig = px.bar(top10, x=col_station, y="승하합계", text="승하합계", title=f"{date_sel} / {line_sel} Top10")
fig.update_traces(marker_color=colors, textposition="outside")
fig.update_layout(xaxis_tickangle=-45, height=600)

st.plotly_chart(fig, use_container_width=True)
