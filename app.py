import streamlit as st


EXERCISE_DB = {
    "유산소(기본)": {
        "걷기": (0.50, 0.60),
        "파워 워킹": (0.55, 0.65),
        "조깅": (0.60, 0.70),
        "달리기": (0.70, 0.80),
        "트레드밀(러닝머신)": (0.65, 0.80),
        "실외 자전거": (0.60, 0.80),
        "실내 자전거(스피닝)": (0.70, 0.85),
        "계단 오르기(스텝퍼)": (0.70, 0.85),
        "일립티컬": (0.60, 0.80),
        "로잉(실내 로잉머신)": (0.70, 0.85),
    },
    "스포츠 경기": {
        "축구": (0.70, 0.90),
        "농구": (0.75, 0.90),
        "배드민턴": (0.65, 0.85),
        "테니스": (0.70, 0.90),
        "골프": (0.55, 0.75),
        "스쿼시": (0.80, 0.90),
    },
    "수중·기타 유산소": {
        "수영(자유형 중심)": (0.60, 0.80),
        "아쿠아로빅": (0.50, 0.70),
        "줄넘기": (0.75, 0.90),
        "등산(트레킹)": (0.60, 0.80),
    },
    "근력·서킷": {
        "웨이트 트레이닝(일반)": (0.50, 0.70),
        "서킷 트레이닝": (0.70, 0.85),
        "크로스핏·메트콘": (0.80, 0.90),
        "고강도 서킷": (0.70, 0.85),
    },
    "재활·저강도": {
        "스트레칭·요가": (0.40, 0.60),
        "필라테스": (0.45, 0.65),
        "가벼운 재활 운동": (0.40, 0.55),
    },
}


def calculate_target_hr(age: int, resting_hr: int, intensity: float) -> tuple[int, float]:
    """Karvonen 공식으로 최대 심박수와 목표 심박수를 계산한다."""
    max_hr = 220 - age
    target_hr = (max_hr - resting_hr) * intensity + resting_hr
    return max_hr, target_hr


def intensity_message(intensity: float) -> tuple[str, str]:
    if intensity < 0.50:
        return "저강도: 회복 및 가벼운 활동에 적합합니다.", "info"
    if intensity < 0.60:
        return "가벼운 강도(50~60%): 재활과 워밍업에 적합합니다.", "success"
    if intensity < 0.70:
        return "중간 강도(60~70%): 체지방 연소와 유산소 운동에 적합합니다.", "info"
    if intensity < 0.80:
        return "중고강도(70~80%): 심폐 지구력 향상에 적합합니다.", "warning"
    return "고강도(80~90%): 인터벌 및 퍼포먼스 운동 구간입니다.", "error"


st.set_page_config(page_title="운동 종목별 목표 심박수", page_icon="❤️", layout="centered")

st.title("❤️ 운동 종목별 목표 심박수 계산기")
st.caption("Karvonen 공식(HRR)으로 운동 종목과 강도에 맞는 목표 심박수를 계산합니다.")

with st.form("heart-rate-form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("나이(세)", min_value=1, max_value=120, value=28)
    with col2:
        resting_hr = st.number_input(
            "안정 시 심박수(bpm)", min_value=30, max_value=120, value=60
        )

    category = st.selectbox("운동 카테고리", list(EXERCISE_DB))
    exercise = st.selectbox("운동 종목", list(EXERCISE_DB[category]))

    min_intensity, max_intensity = EXERCISE_DB[category][exercise]
    intensity = st.slider(
        "운동 강도(HRR 비율)",
        min_value=float(min_intensity),
        max_value=float(max_intensity),
        value=round((min_intensity + max_intensity) / 2, 2),
        step=0.01,
        format="%.0f%%",
        help="선택한 운동의 권장 범위 안에서 현재 운동 강도를 조정하세요.",
    )
    st.caption(
        f"권장 범위: {min_intensity:.0%}~{max_intensity:.0%} · 선택: {intensity:.0%}"
    )
    submitted = st.form_submit_button("목표 심박수 계산", use_container_width=True)

if submitted:
    max_hr, target_hr = calculate_target_hr(int(age), int(resting_hr), intensity)
    st.subheader("계산 결과")
    col1, col2 = st.columns(2)
    col1.metric("운동 종목", exercise)
    col2.metric("선택 강도", f"{intensity:.0%}")
    col1.metric("추정 최대 심박수", f"{max_hr} bpm")
    col2.metric("목표 심박수", f"{target_hr:.0f} bpm")

    message, message_type = intensity_message(intensity)
    getattr(st, message_type)(message)

    if resting_hr >= max_hr:
        st.warning("안정 시 심박수가 추정 최대 심박수 이상입니다. 입력값을 확인해 주세요.")

st.divider()
st.caption("이 계산은 운동 참고용이며 의료 진단이나 처방을 대신하지 않습니다.")
