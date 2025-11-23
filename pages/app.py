import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# 1. 파일 로드 및 데이터 분석
@st.cache_data
def load_data(dessert_path, cafe_path):
    """CSV 파일을 로드하고 '날짜' 열을 datetime 형식으로 변환합니다."""
    # DESSERT.csv 로드 및 날짜 처리
    df_dessert = pd.read_csv(dessert_path)
    df_dessert['날짜'] = pd.to_datetime(df_dessert['날짜'])
    df_dessert = df_dessert.set_index('날짜').sort_index()

    # CAFE.csv 로드
    df_cafe = pd.read_csv(cafe_path)

    return df_dessert, df_cafe

# 4. Plotly 그래프 생성
def create_line_chart(df, dessert_name, start_date, end_date):
    """선택된 기간 및 디저트에 대한 Plotly 라인 그래프를 생성합니다."""
    # 선택된 기간으로 데이터 필터링
    df_filtered = df.loc[start_date:end_date, [dessert_name]]

    # Plotly 그래프 생성
    fig = px.line(
        df_filtered,
        x=df_filtered.index,
        y=dessert_name,
        title=f"📅 {start_date.strftime('%Y-%m-%d')}부터 {end_date.strftime('%Y-%m-%d')}까지의 **{dessert_name}** 검색량 변화",
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

    fig.update_traces(mode='lines+markers')
    return fig

# 2. 스트림릿에서 작동되는 코드
def main():
    # --- 9. 베이지와 갈색 조합의 테마 설정 (Style) ---
    st.markdown("""
        <style>
            .stApp {
                background-color: #FFF8E1; /* 라이트 베이지 배경 */
                color: #5D4037; /* 진한 갈색 글씨 */
            }
            .stButton>button {
                background-color: #A0522D; /* 시에나 (갈색) 버튼 배경 */
                color: white;
                border-radius: 10px;
                border: none;
                padding: 10px 24px;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #8B4513; /* 더 진한 갈색 */
            }
            .stSelectbox div[role="listbox"] {
                background-color: #F5F5DC; /* 베이지색 드롭다운 배경 */
            }
            h1, h2, h3 {
                color: #5D4037; /* 진한 갈색 헤더 */
            }
        </style>
        """, unsafe_allow_html=True)

    st.title("🍰 디저트 트렌드 & 카페 추천 서비스")
    st.markdown("---")

    # 데이터 로드
    df_dessert, df_cafe = load_data("CAFE.csv", "DESSERT.csv")

    # 모든 디저트 이름 (첫 번째 열 '날짜' 제외)
    dessert_options = df_dessert.columns.tolist()

    # --- 사이드바: 3. 디저트와 기간을 선택하게 해줘 ---
    st.sidebar.header("🔍 검색 옵션")

    # 디저트 선택
    selected_dessert = st.sidebar.selectbox(
        "**디저트 선택:**",
        options=dessert_options,
        index=0
    )

    # 기간 설정
    min_date = df_dessert.index.min().date()
    max_date = df_dessert.index.max().date()

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "**시작 날짜:**",
            min_value=min_date,
            max_value=max_date,
            value=min_date,
            key='start_date'
        )
    with col2:
        end_date = st.date_input(
            "**종료 날짜:**",
            min_value=min_date,
            max_value=max_date,
            value=max_date,
            key='end_date'
        )

    # 날짜 유효성 검사
    if start_date > end_date:
        st.sidebar.error("시작 날짜는 종료 날짜보다 빠를 수 없습니다.")
        return

    # --- 메인 영역: 4. Plotly 그래프 출력 ---
    st.header(f"📈 {selected_dessert} 검색 트렌드")
    fig = create_line_chart(df_dessert, selected_dessert, start_date, end_date)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- 6. 선택한 디저트를 판매하는 카페를 추천해드릴까요? (Yes/No) ---
    st.header("📍 맞춤형 카페 추천")

    st.subheader("선택한 디저트를 판매하는 카페를 추천해드릴까요?")
    
    # 7. 만약 no라면 거기서 멈추고 yes라면 5번의 데이터에 맞는 카페를 소개해줘
    col_yes, col_no, _ = st.columns([1, 1, 4])
    with col_yes:
        yes_button = st.button("✅ Yes")
    with col_no:
        no_button = st.button("❌ No")

    if yes_button:
        # 5. CAFE 파일 데이터 판다스로 분석해줘 (이미 load_data에서 분석됨)
        # 선택한 디저트와 매칭되는 카페 정보 필터링
        recommended_cafes = df_cafe[df_cafe['디저트'] == selected_dessert]

        if not recommended_cafes.empty:
            st.success(f"🥳 **{selected_dessert}**를 판매하는 추천 카페입니다!")
            
            # 카페 정보 테이블 출력
            st.dataframe(
                recommended_cafes[['디저트', '카페1', '위치1', '카페2', '위치2', '비고']]
                .rename(columns={'카페1': '추천 카페 A', '위치1': '위치 A', '카페2': '추천 카페 B', '위치2': '위치 B'}),
                use_container_width=True
            )

            # 지도 링크 추가 (선택 사항)
            for _, row in recommended_cafes.iterrows():
                st.markdown(f"""
                * **{row['카페1']}** 위치: [{row['위치1']}](https://map.naver.com/v5/search/{row['위치1']} 'Naver Map으로 이동')
                * **{row['카페2']}** 위치: [{row['위치2']}](https://map.naver.com/v5/search/{row['위치2']} 'Naver Map으로 이동')
                """)
        else:
            st.warning(f"😔 **{selected_dessert}**에 대한 추천 카페 정보를 찾을 수 없습니다.")

    elif no_button:
        st.info("알겠습니다. 다음에 필요하면 다시 요청해주세요! 👋")

if __name__ == "__main__":
    main()
