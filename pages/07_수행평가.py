import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from pathlib import Path

# ---------- Config ----------
st.set_page_config(page_title="디저트 트렌드 & 카페 추천", layout="wide")
BASE_PATH = Path("/mnt/data")
DESSERT_CSV = BASE_PATH / "DESSERT.csv.csv"
CAFE_CSV = BASE_PATH / "CAFE.csv.csv"

# ---------- Styling (beige / brown) ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #F7EFE6 0%, #E9DCC9 100%);
        color: #3E2723;
    }
    .sidebar .sidebar-content {
        background: #E7D4BF;
    }
    .stButton>button {
        background-color: #8D6E63;
        color: white;
    }
    .big-title {
        font-size:32px;
        font-weight:700;
        color:#4E342E;
    }
    .muted {
        color:#5D4037;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="big-title">🍰 디저트 트렌드 탐색 & 카페 추천</div>', unsafe_allow_html=True)
st.markdown("선택한 기간 내에 디저트가 얼마나 검색(언급)되었는지 시각화하고, 해당 디저트를 판매하는 카페를 추천합니다. (UI 색상은 카페 분위기 — 베이지/갈색 계열)")

# ---------- Helpers to detect columns ----------
def detect_date_column(df):
    for c in df.columns:
        lc = c.lower()
        if "date" in lc or "day" in lc or "time" in lc:
            return c
    # fallback: first datetime-like column
    for c in df.columns:
        try:
            pd.to_datetime(df[c])
            return c
        except Exception:
            continue
    return None

def detect_count_column(df):
    # common names
    for c in df.columns:
        lc = c.lower()
        if any(x in lc for x in ["count","search","mentions","value","hits","freq","frequency"]):
            return c
    # fallback numeric column (excluding obvious id columns)
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        return numeric_cols[0]
    return None

# ---------- Load data ----------
@st.cache_data
def load_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"파일을 불러오지 못했습니다: {path}\\n에러: {e}")
        return None

dessert_df = load_csv(DESSERT_CSV)
cafe_df = load_csv(CAFE_CSV)

if dessert_df is None:
    st.stop()

# ---------- Analyze DESSERT.csv ----------
st.header("1) DESSERT.csv 데이터 확인")
st.write("파일 경로:", str(DESSERT_CSV))
st.write("기본 정보:")
st.write(f"- 행: {len(dessert_df)}, 열: {len(dessert_df.columns)}")
st.dataframe(dessert_df.head(10))

date_col = detect_date_column(dessert_df)
count_col = detect_count_column(dessert_df)
dessert_col = None
for c in dessert_df.columns:
    if "dessert" in c.lower() or "name" in c.lower() or "item" in c.lower():
        dessert_col = c
        break
# fallback: try to find a column with few unique values and string type (likely dessert names)
if dessert_col is None:
    string_cols = dessert_df.select_dtypes(include=["object"]).columns.tolist()
    for c in string_cols:
        if 1 < dessert_df[c].nunique() < max(50, len(dessert_df)//5):
            dessert_col = c
            break

if date_col is None or dessert_col is None or count_col is None:
    st.warning("파일에서 주요 컬럼(날짜, 디저트명, 카운트)을 자동으로 찾지 못했을 수 있습니다. 아래 선택 박스로 수동 지정하세요.")
    col1, col2, col3 = st.columns(3)
    with col1:
        date_col = st.selectbox("날짜 컬럼 선택", ["(자동탐지 실패)"] + list(dessert_df.columns), index=0 if date_col is None else list(dessert_df.columns).index(date_col)+1)
    with col2:
        dessert_col = st.selectbox("디저트 이름 컬럼 선택", ["(자동탐지 실패)"] + list(dessert_df.columns), index=0 if dessert_col is None else list(dessert_df.columns).index(dessert_col)+1)
    with col3:
        count_col = st.selectbox("검색수/카운트 컬럼 선택", ["(자동탐지 실패)"] + list(dessert_df.columns), index=0 if count_col is None else list(dessert_df.columns).index(count_col)+1)

# Try to parse dates
try:
    dessert_df[date_col] = pd.to_datetime(dessert_df[date_col])
except Exception:
    st.error(f"선택한 날짜 컬럼({date_col})을 날짜로 변환하지 못했습니다. 데이터 형식을 확인해주세요.")
    st.stop()

# Sidebar UI: dessert & date range
st.sidebar.header("검색 조건")
desserts_unique = sorted(dessert_df[dessert_col].dropna().astype(str).unique())
selected_dessert = st.sidebar.selectbox("디저트를 선택하세요", desserts_unique)
min_date = dessert_df[date_col].min().date()
max_date = dessert_df[date_col].max().date()
default_start = max_date - datetime.timedelta(days=30)
selected_range = st.sidebar.date_input("기간 선택 (시작, 종료)", value=(default_start, max_date), min_value=min_date, max_value=max_date)

if len(selected_range) != 2:
    st.error("기간은 시작과 종료, 두 날짜를 입력해야 합니다.")
    st.stop()
start_date, end_date = selected_range
start_dt = pd.to_datetime(start_date)
end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

# Filter data
mask = (dessert_df[date_col] >= start_dt) & (dessert_df[date_col] <= end_dt) & (dessert_df[dessert_col].astype(str) == str(selected_dessert))
filtered = dessert_df.loc[mask].copy()
st.subheader(f"선택: {selected_dessert} — {start_date} 부터 {end_date} 까지")
st.write(f"기간 내 총 관측치: {len(filtered)}")

if len(filtered) == 0:
    st.info("선택한 기간/디저트의 데이터가 없습니다. 전체 디저트 트렌드를 대신 보여드립니다.")
    # show aggregated trend for that dessert name across all dates
    agg = dessert_df.groupby(pd.Grouper(key=date_col, freq="D"))[count_col].sum().reset_index()
else:
    agg = filtered.groupby(pd.Grouper(key=date_col, freq="D"))[count_col].sum().reset_index()

# Fill missing days
agg = agg.set_index(date_col).asfreq("D", fill_value=0).reset_index()

# Plot with plotly
st.header("2) 트렌드 그래프 (Plotly)")
fig = px.line(agg, x=date_col, y=count_col, title=f"{selected_dessert} 검색량 추이", markers=True)
fig.update_layout(template="plotly_white",
                  plot_bgcolor="rgba(0,0,0,0)",
                  paper_bgcolor="rgba(0,0,0,0)",
                  xaxis_title="날짜",
                  yaxis_title="검색 수 / 언급 수")
st.plotly_chart(fig, use_container_width=True)

# Simple stats
st.header("3) 간단 통계")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("기간 합계", int(agg[count_col].sum()))
with col_b:
    st.metric("평균(일)", round(float(agg[count_col].mean()),2))
with col_c:
    st.metric("최대값(일)", int(agg[count_col].max()))

# ---------- CAFE.csv analysis ----------
st.header("4) CAFE.csv 데이터 확인")
if cafe_df is None:
    st.warning("CAFE.csv 파일이 없습니다. 추천 기능을 사용하려면 파일을 업로드하세요.")
    cafe_df = pd.DataFrame()
else:
    st.write("파일 경로:", str(CAFE_CSV))
    st.write("기본 정보:")
    st.write(f"- 행: {len(cafe_df)}, 열: {len(cafe_df.columns)}")
    st.dataframe(cafe_df.head(10))

# Ask user if they'd like recommendations
st.header("5) 카페 추천")
want_reco = st.radio("선택한 디저트를 판매하는 카페를 추천해드릴까요?", ("Yes", "No"))

if want_reco == "No":
    st.info("요청하신 대로 카페 추천을 중단합니다. 다른 디저트/기간으로 다시 시도해 주세요.")
else:
    if cafe_df is None or cafe_df.empty:
        st.warning("CAFE.csv 데이터가 없어서 추천을 제공할 수 없습니다.")
    else:
        # Try to find cafe columns
        cafe_name_col = None
        cafe_menu_col = None
        cafe_addr_col = None
        cafe_score_col = None
        for c in cafe_df.columns:
            lc = c.lower()
            if any(x in lc for x in ["name","cafe","shop"]):
                cafe_name_col = cafe_name_col or c
            if any(x in lc for x in ["menu","dessert","items","product"]):
                cafe_menu_col = cafe_menu_col or c
            if any(x in lc for x in ["addr","address","location","place"]):
                cafe_addr_col = cafe_addr_col or c
            if any(x in lc for x in ["score","rating","rate","stars"]):
                cafe_score_col = cafe_score_col or c

        # fallback defaults
        if cafe_name_col is None:
            cafe_name_col = cafe_df.columns[0]
        if cafe_menu_col is None:
            # try a string column with many unique values
            for c in cafe_df.select_dtypes(include=["object"]).columns:
                if cafe_df[c].astype(str).str.contains(str(selected_dessert), case=False).any():
                    cafe_menu_col = c
                    break
            if cafe_menu_col is None:
                cafe_menu_col = cafe_df.select_dtypes(include=["object"]).columns[0] if len(cafe_df.columns)>0 else None

        # Filter cafes that mention the dessert (case-insensitive substring match)
        mask_cafe = cafe_df[cafe_menu_col].astype(str).str.contains(str(selected_dessert), case=False, na=False)
        matches = cafe_df.loc[mask_cafe].copy()
        if matches.empty:
            st.info("데이터에서 해당 디저트를 판매하는 카페를 찾지 못했습니다. (CAFE.csv의 메뉴/설명 컬럼을 확인하세요)")
        else:
            # Sort by score if exists
            if cafe_score_col and cafe_score_col in matches.columns:
                try:
                    matches[cafe_score_col] = pd.to_numeric(matches[cafe_score_col], errors="coerce")
                    matches = matches.sort_values(by=cafe_score_col, ascending=False)
                except Exception:
                    pass

            st.subheader(f"'{selected_dessert}'을(를) 판매하는 카페 추천 ({len(matches)}곳)")
            display_cols = [c for c in [cafe_name_col, cafe_menu_col, cafe_addr_col, cafe_score_col] if c and c in matches.columns]
            st.dataframe(matches[display_cols].reset_index(drop=True))

            # Show map if lat/lon columns exist
            lat_col = None
            lon_col = None
            for c in matches.columns:
                if "lat" in c.lower():
                    lat_col = c
                if "lon" in c.lower() or "lng" in c.lower():
                    lon_col = c
            if lat_col and lon_col:
                st.subheader("위치 지도")
                try:
                    map_df = matches[[lat_col, lon_col]].dropna()
                    map_df = map_df.rename(columns={lat_col:"lat", lon_col:"lon"})
                    st.map(map_df)
                except Exception:
                    pass

st.markdown("---")
st.markdown("앱 제작자: 자동 생성 스크립트 • 색상 테마: 베이지/갈색")
