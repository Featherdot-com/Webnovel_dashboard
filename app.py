import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="웹소설 시장 분석", page_icon="📚", layout="wide")
st.markdown("""
<style>
    .stApp { background: #f7f9fc; color: #1f2937; }
    [data-testid="stHeader"] { background: rgba(247,249,252,0.92); }
    [data-testid="stSidebar"] { background: #111827; }
    [data-testid="stSidebar"] * { color: #f9fafb !important; }
    .hero { background: linear-gradient(135deg, #312e81 0%, #4f46e5 55%, #7c3aed 100%); padding: 2rem 2.2rem; border-radius: 22px; color: white; margin-bottom: 1.4rem; box-shadow: 0 12px 30px rgba(49,46,129,.18); }
    .hero h1 { color: white; margin: 0 0 .35rem 0; font-size: 2.35rem; }
    .hero p { color: #e0e7ff; margin: 0; font-size: 1rem; }
    [data-testid="stMetric"] { background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1rem 1.1rem; box-shadow: 0 4px 14px rgba(15,23,42,.05); }
    [data-testid="stMetricLabel"] { color: #64748b; }
    [data-testid="stMetricValue"] { color: #312e81; }
    h2 { color: #312e81; border-left: 5px solid #6366f1; padding-left: .65rem; margin-top: 2rem; }
    h3 { color: #4338ca; }
    .notice { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 14px; padding: 1rem 1.2rem; color: #7c2d12; margin: .8rem 0 1.2rem 0; }
    .stDataFrame { border-radius: 14px; overflow: hidden; }
    div[data-testid="stPlotlyChart"] { background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: .7rem; box-shadow: 0 4px 14px rgba(15,23,42,.04); }
    .stButton > button, .stDownloadButton > button { border-radius: 10px; border: 1px solid #c7d2fe; color: #3730a3; background: #eef2ff; }
</style>
<div class="hero">
  <h1>📚 웹소설 시장 분석</h1>
  <p>공급량 · 랭킹 진입 · 인기 작품 표본 · 이용 이유를 한눈에 확인하는 대시보드</p>
</div>
<div class="notice"><b>분석 주의:</b> 조회수와 인기 순위는 2026년 10월 5일 15:00 기준 카카오페이지 인기 10개 작품의 표본입니다. 작품별 연재 기간과 누적 기준이 다를 수 있으므로 절대적인 독자 수요가 아닌 간접 지표로만 해석합니다.</div>
""", unsafe_allow_html=True)

ANNUAL = pd.DataFrame({
    "연도": [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026],
    "발행 종수": [869,1455,1780,1898,2150,2836,3575,4025,6460,6460,8443,8878,9500],
})
ANNUAL["비고"] = ""
ANNUAL.loc[ANNUAL["연도"] == 2026, "비고"] = "7.7개월 기준 약 9,500종"

GENRE_6M = pd.DataFrame({
    "장르": ["로맨스","로판","현판","판타지","무협","BL"],
    "공급": [16167,7501,5983,7747,4172,4956],
    "랭킹 진입": [213,426,330,413,217,32],
    "진입률": [0.013,0.057,0.055,0.053,0.052,0.006],
    "TOP100 진입률": [0.0066,0.0313,0.0226,0.0245,0.0242,0.0008],
})

GENRE_2Y = pd.DataFrame({
    "장르": ["무협","판타지","현판","로판","로맨스","BL"],
    "공급": [857,2310,2155,2076,2991,1031],
    "랭킹 진입": [99,223,210,189,163,23],
    "진입률": [0.116,0.101,0.097,0.091,0.054,0.022],
})

REASONS = pd.DataFrame({
    "이용 이유": ["시간과 장소에 관계없이 이용할 수 있어서","보관과 휴대가 편리해서","무료로 이용할 수 있어서","좋아하는 콘텐츠가 많아서","종이책보다 가격이 저렴해서","구독서비스로 무제한 이용이 가능해서","다양한 기능들이 편리해서","다른 일을 하면서 동시에 이용할 수 있어서","시간을 보내려고"],
    "비율": [33.5,21.4,15.7,9.8,7.5,3.9,0.8,0.4,6.8],
})

TOP10 = pd.DataFrame({
    "순위": range(1, 11),
    "제목": ["흑막을 치료하고 도망치려다 실패함","괴담에 떨어져도 출근을 해야 하는구나","전생 네크로맨서는 헌터가 너무 쉽다","폐급 특성으로 미궁 정복","챌린저급 플레이어의 회귀","소월객잔","마법학교 마법사로 살아가는 법","변경백 서자는 황제였다","의원, 다시 살다","은해상단 막내아들"],
    "장르": ["로판","현판","판타지","판타지","판타지","로판","판타지","판타지","무협","무협"],
    "조회수 원문": ["392.9k","465.1M","336.1K","3.7M","1.1M","1.6M","345.8M","177.8M","328.7M","125.7M"],
    "조회수": [392900,465100000,336100,3700000,1100000,1600000,345800000,177800000,328700000,125700000],
    "평점": [9.7,10.0,8.8,9.3,9.1,9.9,9.9,10.0,9.9,9.6],
})

st.title("📚 웹소설 시장 수요·공급 분석")
st.caption("현재 확보된 자료를 이용한 분석 대시보드 | 데이터 기준: 파일별 원본 기준")

with st.sidebar:
    st.header("분석 지표 안내")
    st.info("조회수·평점·인기순위는 2026-10-05 15:00 카카오페이지 인기 10개 작품의 표본입니다.")
    st.warning("조회수는 작품별 연재 기간과 누적 기준이 다를 수 있습니다. 절대적인 독자 수요가 아니라 특정 시점 인기 작품 표본의 간접 지표로만 해석하세요.")
    st.write("**추가 유의사항**")
    st.markdown("- 인기 10개만 포함한 표본입니다.\n- 한 플랫폼과 한 시점의 자료입니다.\n- 조회수는 작품 연령·프로모션·노출에 영향을 받을 수 있습니다.\n- 랭킹 진입률은 독자 반응 외에 플랫폼 랭킹 기준의 영향을 받습니다.\n- 전체 장르 수요나 전체 독자 비율로 일반화하지 않습니다.\n- 웹툰 사업체 매출 자료는 웹소설 수요 지표로 사용하지 않습니다.")

st.header("핵심 요약")
c1, c2, c3, c4 = st.columns(4)
c1.metric("인기 표본", "10개 작품")
c2.metric("가장 많이 나타난 장르", "판타지", "5개")
c3.metric("전체 발행량(2025)", "8,878종")
c4.metric("이용 이유 1위", "시간·장소 무관", "33.5%")

st.header("1. 연도별 웹소설 발행 종수")
st.line_chart(ANNUAL.set_index("연도")["발행 종수"])
st.dataframe(ANNUAL, use_container_width=True, hide_index=True)
st.caption("2026년은 7.7개월 기준 약 9,500종이므로 완전한 연도와 직접 비교하지 않습니다.")

st.header("2. 장르별 공급과 랭킹 진입")
period = st.radio("기간 선택", ["최근 6개월", "2025~2026년 발행분"], horizontal=True)
genre = GENRE_6M if period == "최근 6개월" else GENRE_2Y
col1, col2 = st.columns(2)
with col1:
    st.subheader("공급량")
    st.bar_chart(genre.set_index("장르")["공급"])
with col2:
    st.subheader("진입률")
    st.bar_chart((genre.set_index("장르")["진입률"] * 100).rename("진입률(%)"))
st.dataframe(genre.style.format({"진입률": "{:.1%}", "TOP100 진입률": "{:.2%}"}), use_container_width=True, hide_index=True)
st.warning("진입률은 실제 독자 수가 아니라 공급 대비 랭킹 진입의 간접 지표입니다.")

st.header("3. 카카오페이지 인기 10위 표본")
st.caption("기준: 2026년 10월 5일 15:00 | 조회수와 평점은 사용자가 제공한 원자료")
left, right = st.columns([1, 1])
with left:
    genre_counts = TOP10["장르"].value_counts().rename_axis("장르").reset_index(name="작품 수")
    st.plotly_chart(px.bar(genre_counts, x="장르", y="작품 수", title="인기 10위 장르 분포"), use_container_width=True)
with right:
    st.plotly_chart(px.scatter(TOP10, x="장르", y="조회수", size="조회수", color="평점", hover_name="제목", log_y=True, title="장르별 조회수 표본"), use_container_width=True)
st.dataframe(TOP10[["순위","제목","장르","조회수 원문","평점"]], use_container_width=True, hide_index=True)
st.info("이 표본에서 판타지 5개, 로판 2개, 무협 2개, 현판 1개가 확인됩니다. 이는 인기 10개 표본의 구성이지 전체 독자 비율이 아닙니다.")

st.header("4. 웹소설 이용 이유")
col1, col2 = st.columns([1.2, 1])
with col1:
    st.plotly_chart(px.bar(REASONS.sort_values("비율"), x="비율", y="이용 이유", orientation="h", text="비율", title="전체 응답자 675명의 이용 이유"), use_container_width=True)
with col2:
    st.dataframe(REASONS.style.format({"비율": "{:.1f}%"}), use_container_width=True, hide_index=True)

st.header("5. 분석 범위와 한계")
st.markdown("""
현재 화면의 장르 수요 해석은 **직접적인 독자 수요 측정이 아니라 간접 분석**입니다.

- 공급: 연도별 발행 종수와 기간별 장르 공급량
- 시장 반응의 간접 지표: 랭킹 진입 수, 공급 대비 진입률, TOP100 진입률
- 특정 시점 인기 지표: 카카오페이지 인기 10위 작품의 장르, 조회수, 평점
- 이용 동기: 전체 응답자 675명의 웹소설 이용 이유

조회수는 작품별 연재 기간, 누적 집계 방식, 프로모션, 노출량 및 작품별 노출 기간이 다를 수 있습니다. 따라서 조회수를 작품 간 또는 장르 간의 절대적인 독자 수요로 비교하지 않고, **2026년 10월 5일 15:00 기준 인기 작품 표본의 관찰값**으로만 사용합니다.

현재 데이터만으로는 장르별 전체 조회수, 구매 수, 구독자 수, 찜 수, 작품별 연재 기간을 알 수 없습니다. 이 데이터가 확보되기 전에는 장르별 전체 독자 수요나 장르 선호도를 확정하지 않습니다.
""")

st.caption("원본 Excel 파일은 수정하지 않았으며, 웹툰 사업체 매출 구간 자료는 웹소설 장르 수요 분석에서 제외했습니다.")

