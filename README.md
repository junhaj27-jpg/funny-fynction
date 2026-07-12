# 운동 종목별 목표 심박수 계산기

운동 종목과 강도를 선택하면 Karvonen 공식(HRR)을 이용해 목표 심박수를 계산하는 Streamlit 앱입니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 계산식

```text
최대 심박수 = 220 - 나이
목표 심박수 = (최대 심박수 - 안정 시 심박수) × 운동 강도 + 안정 시 심박수
```

계산 결과는 일반적인 운동 참고용이며 의료 진단이나 처방을 대신하지 않습니다.
