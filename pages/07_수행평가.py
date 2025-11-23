import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# --- 1. 파일 로드 및 데이터 분석 (인코딩 안정성 강화) ---
@st.cache_data
def load_data(dessert_path, cafe_path):
    """CSV 파일을 로드하고 '날짜' 열을 datetime 형식으로 변환합니다."""
    
    # DESSERT.csv 로드 및 날짜 처리
    try:
        df_dessert = pd.read_csv(dessert_path, encoding='utf-8')
    except UnicodeDecodeError:
        df_dessert = pd.read_csv(dessert_path, encoding='cp949') # 윈도우 환경 대응

    df_dessert['날짜'] = pd.to_datetime(df_dessert['날짜'])
    df_dessert = df_dessert.set_index('날짜').sort_index()

    # CAFE.csv 로드
    try:
        df_cafe = pd.read_csv(cafe_path, encoding='utf-8')
    except UnicodeDecodeError:
        df_cafe = pd.read_csv(cafe_path, encoding='cp949') # 윈도우 환경 대응

    # 5. CAFE 파일 데이터 판다스로 분석: CAFE.csv의 '디저트' 열을 기준으로 추천에 사용
    # (이미 로드 완료 및 DataFrame 형태로 준비됨)

    return df_dessert, df_cafe

# --- 4. Plotly 그래프 생성 함수 ---
def create_line_chart(df, dessert_name, start_date, end_date):
    """선택된 기간 및 디저트에 대한 Plotly 라인 그래프를 생성합니다."""
    # 선택된 기간으로 데이터 필터링
    # date 객체를 datetime 객체로 변환하여 필터링
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    # 인덱스가 datetime 형식이라고 가정하고 loc 사용
    df_filtered = df.loc[start_dt:end_dt, [dessert_name]].dropna()

    # Plotly 그래프 생성
    fig = px.line(
        df_filtered,
        x=df_filtered.index,
        y=dessert_name,
        title=f"📅 **{start_date.strftime('%Y-%m-%d')}**부터 **{end_date.strftime('%Y-%m-%d')}**까지의 **{dessert_name}** 검색량 변화",
        labels={'날짜': '날짜', dessert_name: '상대적 검색량'},
        color_discrete_sequence=['#A0522D'] # 시에나 (갈색 계열)
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="상대적 검색량",
        plot_bgcolor='white',
        paper_bgcolor='#FFF8E1', # 미색/베이지 배경
        font_color='#5D4037', # 진한 갈색 글씨
        title_font_size=20,
        hovermode="x unified"
    )

    fig.update_traces(mode='lines+markers', line=dict(width=3))
    return fig

# --- 2. 스트림릿에서 작동되는 코드 (메인 함수) ---
def main():
    # --- 프로그램 배경: 베이지와 갈색 조합의 테마 설정 (Style) ---
    st.markdown("""
        <style>
            /* 전체 앱 배경색 (베이지) */
            .stApp {
                background-color: #FFF8E1; 
                color: #5D4037; 
            }
            /* 버튼 스타일 (갈색) */
            .stButton>button {
                background-color: #A0522D; 
                color: white;
                border-radius: 10px;
                border: none;
                padding: 10px 24px;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #8B4513; 
            }
            /* 헤더 색상 (진한 갈색) */
            h1, h2, h3 {
                color: #5D4037; 
            }
            /* 데이터프레임 헤더 색상 */
            .dataframe th {
                background-color: #D2B48C !important; /* 탄(갈색 계
