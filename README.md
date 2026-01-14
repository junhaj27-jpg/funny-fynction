# funny-fynction
재미있는 파이썬 함수만들기

import streamlit as st

st.set_page_config(page_title="운동 종목별 목표 심박수", page_icon="❤️", layout="centered")

st.title("🏃‍♂️ 운동 종목별 목표 심박수 처방")
st.caption("Karvonen 공식(HRR): 종목 선택 → 권장 강도 범위 내 조정 → 목표 심박수(Target HR) 계산")

st.divider()

# ============================
# 입력
# ============================
age = st.number_input("나이(세)", min_value=1, max_value=120, value=28)
rest_hr = st.number_input("안정시 심박수(bpm)", min_value=30, max_value=120, value=60)

st.divider()

# ============================
# 종목 데이터(권장 HRR 강도 범위: (min, max))
# - 실무에서는 사용자/체력/숙련도에 따라 조정 가능
# ============================
exercise_db = {
    "유산소(기본)": {
        "걷기": (0.50, 0.60),
        "파워워킹": (0.55, 0.65),
        "조깅": (0.60, 0.70),
        "러닝": (0.70, 0.80),
        "트레드밀(러닝머신)": (0.65, 0.80),
        "사이클(자전거)": (0.60, 0.80),
        "실내 자전거(스피닝)": (0.70, 0.85),
        "계단오르기(스텝퍼)": (0.70, 0.85),
        "일립티컬": (0.60, 0.80),
        "로잉(실내 로잉머신)": (0.70, 0.85),
    },
    "스포츠(경기형)": {
        "축구": (0.70, 0.90),
        "농구": (0.75, 0.90),
        "배드민턴": (0.65, 0.85),
        "테니스": (0.70, 0.90),
        "탁구": (0.55, 0.75),
        "스쿼시": (0.80, 0.90),
    },
    "수중/기타 유산소": {
        "수영(자유형 중심)": (0.60, 0.80),
        "아쿠아로빅": (0.50, 0.70),
        "줄넘기": (0.75, 0.90),
        "등산(트레킹)": (0.60, 0.80),
    },
    "근력/서킷(심박 상승형)": {
        "웨이트 트레이닝(일반)": (0.50, 0.70),
        "서킷 트레이닝": (0.70, 0.85),
        "크로스핏/메트콘": (0.80, 0.90),
        "케틀벨 서킷": (0.70, 0.85),
    },
    "재활/저강도": {
        "스트레칭/요가": (0.40, 0.60),
        "필라테스": (0.45, 0.65),
        "가벼운 재활운동": (0.40, 0.55),
    }
}

# ============================
# 선택 UI (카테고리 → 종목)
# ============================
category = st.selectbox("운동 카테고리", list(exercise_db.keys()))
exercise = st.selectbox("운동 종목", list(exercise_db[category].keys()))

min_int, max_int = exercise_db[category][exercise]
default_int = round((min_int + max_int) / 2, 2)

intensity = st.slider(
    "운동강도(HRR 비율) 조정",
    min_value=float(min_int),
    max_value=float(max_int),
    value=float(default_int),
    step=0.01,
    help="선택한 종목의 권장 강도 범위 내에서 조정합니다."
)

st.write(f"권장 범위: **{min_int*100:.0f}% ~ {max_int*100:.0f}%** (현재 선택: **{intensity*100:.0f}%**)")

st.divider()

# ============================
# 계산 버튼
# ============================
if st.button("🎯 목표 심박수 계산"):
    hr_max = 220 - age
    target_hr = (hr_max - rest_hr) * intensity + rest_hr

    st.subheader("📊 결과(값만 표시)")
    st.metric("운동 종목", exercise)
    st.metric("선택 강도(HRR)", f"{intensity*100:.0f}%")
    st.metric("HRmax", f"{hr_max} bpm")
    st.metric("🎯 목표 심박수(Target HR)", f"{target_hr:.1f} bpm")

    # 구간 안내(당신이 준 구간 기반)
    if 0.50 <= intensity < 0.60:
        st.success("가벼움(50–60%): 재활, 워밍업")
    elif 0.60 <= intensity < 0.70:
        st.info("중간(60–70%): 체지방 연소, 유산소")
    elif 0.70 <= intensity < 0.80:
        st.warning("중고강도(70–80%): 심폐지구력 향상")
    elif 0.80 <= intensity <= 0.90:
        st.error("고강도(80–90%): 인터벌, 퍼포먼스")
    else:
        st.write("선택 강도가 권장 구간(50–90%) 밖입니다. 종목/범위를 다시 확인하세요.")

