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
        "가벼운 산책": (0.40, 0.55),
        "노르딕 워킹": (0.55, 0.70),
        "트레일 러닝": (0.70, 0.90),
        "인라인 스케이트": (0.65, 0.85),
        "에어로빅": (0.65, 0.85),
        "줌바": (0.65, 0.85),
    },
    "스포츠 경기": {
        "축구": (0.70, 0.90),
        "농구": (0.75, 0.90),
        "배드민턴": (0.65, 0.85),
        "테니스": (0.70, 0.90),
        "골프": (0.55, 0.75),
        "스쿼시": (0.80, 0.90),
        "탁구": (0.55, 0.75),
        "배구": (0.65, 0.85),
        "야구·소프트볼": (0.55, 0.75),
        "핸드볼": (0.75, 0.90),
        "풋살": (0.75, 0.90),
        "럭비": (0.75, 0.90),
        "복싱": (0.75, 0.90),
        "태권도·격투기": (0.70, 0.90),
    },
    "수중·기타 유산소": {
        "수영(자유형 중심)": (0.60, 0.80),
        "아쿠아로빅": (0.50, 0.70),
        "줄넘기": (0.75, 0.90),
        "등산(트레킹)": (0.60, 0.80),
        "접영·평영 수영": (0.70, 0.85),
        "카약·카누": (0.60, 0.80),
        "서핑": (0.60, 0.80),
        "크로스컨트리 스키": (0.70, 0.90),
    },
    "근력·서킷": {
        "웨이트 트레이닝(일반)": (0.50, 0.70),
        "서킷 트레이닝": (0.70, 0.85),
        "크로스핏·메트콘": (0.80, 0.90),
        "고강도 서킷": (0.70, 0.85),
        "케틀벨 운동": (0.65, 0.85),
        "맨몸 운동": (0.55, 0.75),
        "HIIT": (0.80, 0.95),
        "클라이밍": (0.65, 0.85),
    },
    "재활·저강도": {
        "스트레칭·요가": (0.40, 0.60),
        "필라테스": (0.45, 0.65),
        "가벼운 재활 운동": (0.40, 0.55),
        "실버 체조": (0.40, 0.55),
        "수중 걷기": (0.40, 0.60),
        "저강도 실내 자전거": (0.45, 0.60),
    },
    "직접 설정": {"목록에 없는 운동": (0.40, 0.95)},
}


def calculate_target_hr(age: int, resting_hr: int, intensity: float) -> tuple[int, float]:
    """Karvonen 공식으로 최대 심박수와 목표 심박수를 계산한다."""
    max_hr = 220 - age
    target_hr = (max_hr - resting_hr) * intensity + resting_hr
    return max_hr, target_hr


def calculate_target_range(
    age: int, resting_hr: int, min_intensity: float, max_intensity: float
) -> tuple[int, float, float]:
    """카보넨 공식으로 권장 목표 심박수 범위를 계산한다."""
    max_hr, low_hr = calculate_target_hr(age, resting_hr, min_intensity)
    _, high_hr = calculate_target_hr(age, resting_hr, max_intensity)
    return max_hr, low_hr, high_hr


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

    if category == "직접 설정":
        custom_exercise = st.text_input("운동 이름", value="사용자 지정 운동")
        exercise = custom_exercise.strip() or "사용자 지정 운동"

    min_intensity, max_intensity = EXERCISE_DB[category][exercise]
    intensity_percent = st.slider(
        "운동 강도(HRR 비율, %)",
        min_value=int(min_intensity * 100),
        max_value=int(max_intensity * 100),
        value=round((min_intensity + max_intensity) * 50),
        step=1,
        format="%d%%",
        help="선택한 운동의 권장 범위 안에서 현재 운동 강도를 조정하세요.",
    )
    intensity = intensity_percent / 100
    st.caption(
        f"권장 범위: {min_intensity:.0%}~{max_intensity:.0%} · 선택: {intensity:.0%}"
    )
    submitted = st.form_submit_button("목표 심박수 계산", use_container_width=True)

if submitted:
    max_hr, target_hr = calculate_target_hr(int(age), int(resting_hr), intensity)
    _, low_hr, high_hr = calculate_target_range(
        int(age), int(resting_hr), min_intensity, max_intensity
    )
    st.subheader("계산 결과")
    col1, col2 = st.columns(2)
    col1.metric("운동 종목", exercise)
    col2.metric("선택 강도", f"{intensity:.0%}")
    col1.metric("추정 최대 심박수", f"{max_hr} bpm")
    col2.metric("선택 강도의 목표 심박수", f"{target_hr:.0f} bpm")
    st.metric("종목 권장 목표 심박수 범위", f"{low_hr:.0f}~{high_hr:.0f} bpm")

    with st.expander("카보넨 공식 계산 과정 보기"):
        st.write(f"최대 심박수 = 220 - {int(age)} = **{max_hr} bpm**")
        st.write(f"심박수 여유분(HRR) = {max_hr} - {int(resting_hr)} = **{max_hr - int(resting_hr)} bpm**")
        st.write(
            f"목표 심박수 = ({max_hr} - {int(resting_hr)}) × {intensity:.0%} "
            f"+ {int(resting_hr)} = **{target_hr:.0f} bpm**"
        )

    message, message_type = intensity_message(intensity)
    getattr(st, message_type)(message)

    if resting_hr >= max_hr:
        st.warning("안정 시 심박수가 추정 최대 심박수 이상입니다. 입력값을 확인해 주세요.")

st.divider()
st.caption("이 계산은 운동 참고용이며 의료 진단이나 처방을 대신하지 않습니다.")
