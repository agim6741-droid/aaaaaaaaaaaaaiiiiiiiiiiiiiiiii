# app.py
# Streamlit app that displays Seoul's top 10 tourist spots (popular with foreigners) using Folium.
# Save this file as `app.py` and the requirements content (below) as `requirements.txt`.

import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title='Seoul Top 10 (Folium)', layout='wide')

st.title('서울 Top 10 관광지 (외국인 인기)')
st.markdown('Folium 지도를 사용해 서울의 대표 관광지 10곳을 표시합니다. 마커를 클릭하면 간단한 설명과 외부 링크(있을 경우)를 볼 수 있습니다.')

# Top 10 locations (name, lat, lon, short description, link)
places = [
    {
        'name': 'Gyeongbokgung Palace (경복궁)',
        'lat': 37.579617,
        'lon': 126.977041,
        'desc': '조선의 대표 궁궐. 근정전, 경회루 등 볼거리 풍부.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264348'
    },
    {
        'name': 'Changdeokgung & Huwon (창덕궁/후원)',
        'lat': 37.582604,
        'lon': 126.991002,
        'desc': '유네스코 세계문화유산. 비원(후원) 산책이 유명.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264349'
    },
    {
        'name': 'Bukchon Hanok Village (북촌한옥마을)',
        'lat': 37.5820,
        'lon': 126.9834,
        'desc': '전통 한옥들이 모여 있는 고즈넉한 마을거리.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264357'
    },
    {
        'name': 'Insadong (인사동)',
        'lat': 37.5740,
        'lon': 126.9849,
        'desc': '전통 공예품, 갤러리, 찻집이 많은 문화거리.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264286'
    },
    {
        'name': 'Myeongdong (명동)',
        'lat': 37.5638,
        'lon': 126.9860,
        'desc': '쇼핑과 길거리음식의 중심지. 화장품, 패션 샵이 많음.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264312'
    },
    {
        'name': 'N Seoul Tower (N서울타워, Namsan Tower)',
        'lat': 37.5511694,
        'lon': 126.9882266,
        'desc': '서울 전경을 한눈에 볼 수 있는 전망명소. 케이블카/등산로 접근성 좋음.',
        'link': 'https://www.nseoultower.co.kr/eng/'
    },
    {
        'name': 'Hongdae (홍대 / Hongik Univ. area)',
        'lat': 37.5572,
        'lon': 126.9240,
        'desc': '젊음의 거리, 인디음악, 카페, 스트릿 퍼포먼스가 활발.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264335'
    },
    {
        'name': 'Dongdaemun Design Plaza (DDP / 동대문디자인플라자)',
        'lat': 37.5663,
        'lon': 127.0090,
        'desc': '미래지향적 건축물과 야간 야경, 패션시장의 중심.',
        'link': 'https://www.ddp.or.kr/eng/index.do'
    },
    {
        'name': 'Lotte World Tower & Mall (롯데월드타워, 잠실)',
        'lat': 37.5131,
        'lon': 127.1026,
        'desc': '초고층 전망대와 대형 쇼핑몰, 아쿠아리움 등 복합시설.',
        'link': 'https://www.lwt.co.kr/eng'
    },
    {
        'name': 'Namdaemun Market (남대문시장)',
        'lat': 37.5584,
        'lon': 126.9770,
        'desc': '전통시장으로 기념품과 길거리음식을 즐기기 좋음.',
        'link': 'https://english.visitkorea.or.kr/enu/ATR/SI_EN_3_1_1_1.jsp?cid=264291'
    }
]

# Sidebar controls
st.sidebar.header('지도 설정')
zoom = st.sidebar.slider('확대 수준 (zoom)', min_value=10, max_value=16, value=12)
show_clusters = st.sidebar.checkbox('마커 클러스터 사용', value=True)
show_list = st.sidebar.checkbox('장소 목록 보기', value=True)

# Build Folium map
seoul_center = (37.5665, 126.9780)
m = folium.Map(location=seoul_center, zoom_start=zoom)

if show_clusters:
    cluster = MarkerCluster()
    for p in places:
        html = f"""
        <h4>{p['name']}</h4>
        <p>{p['desc']}</p>
        <a href=\"{p['link']}\" target=\"_blank\">자세히 보기</a>
        """
        folium.Marker(location=(p['lat'], p['lon']), popup=folium.Popup(html, max_width=300)).add_to(cluster)
    cluster.add_to(m)
else:
    for p in places:
        html = f"""
        <h4>{p['name']}</h4>
        <p>{p['desc']}</p>
        <a href=\"{p['link']}\" target=\"_blank\">자세히 보기</a>
        """
        folium.Marker(location=(p['lat'], p['lon']), popup=folium.Popup(html, max_width=300)).add_to(m)

folium.LayerControl().add_to(m)

# Display map
st.subheader('지도')
map_data = st_folium(m, width=900, height=600)

# Optional: show list of places
if show_list:
    st.subheader('Top 10 장소 목록')
    for i, p in enumerate(places, start=1):
        st.markdown(f"**{i}. {p['name']}** — {p['desc']}  ")
        st.markdown(f"위치: {p['lat']}, {p['lon']} — [더 보기]({p['link']})")

# Provide a downloadable requirements.txt content
req_txt = '''
streamlit>=1.24
folium>=0.14.0
streamlit-folium>=0.11.0
pandas>=1.5
branca>=0.6.0
'''

st.sidebar.download_button('requirements.txt 다운로드', data=req_txt, file_name='requirements.txt', mime='text/plain')

# Footer
st.markdown('---')
st.caption('앱: Folium + Streamlit 예시. Streamlit Cloud(현재 이름: Streamlit Community Cloud)에 배포하려면 이 디렉터리에 `app.py`와 `requirements.txt`를 업로드하세요.')

# ---------------------------
# requirements.txt (파일로 저장하세요)
# ---------------------------
# 아래 내용을 `requirements.txt`로 저장하세요:
#
# streamlit>=1.24
# folium>=0.14.0
# streamlit-folium>=0.11.0
# pandas>=1.5
# branca>=0.6.0
#
# 사용법:
# 1) 이 폴더에 app.py 와 requirements.txt 를 저장
# 2) 로컬에서 확인하려면: `streamlit run app.py`
# 3) Streamlit Cloud에 배포하려면, GitHub 리포지토리에 푸시 후 Streamlit에 연결
