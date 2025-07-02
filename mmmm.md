# PHM 2025 센서 데이터 설명 (Sensed Engine Variables)

총 16개의 센서 변수가 포함되어 있으며, 이 중 14개는 주요(primary) 센서로 간주됩니다. 각 변수의 의미, 물리적 위치, 활용 용도를 아래에 정리했습니다.

---

## 📦 센서 변수 상세 설명

| No. | 변수명             | 의미 (영문)                        | 설명 (한글)                                  | 예측/진단 중요도 |
|-----|--------------------|-------------------------------------|-----------------------------------------------|------------------|
| 1   | Sensed_Altitude     | Altitude                            | 비행 중 고도 (피트 또는 미터)                   | ✅ 입력 조건     |
| 2   | Sensed_Mach         | Mach number                         | 비행 마하 수 (속도/음속 비율)                  | ✅ 입력 조건     |
| 3   | Sensed_Pamb         | Ambient pressure                    | 외기압 (대기압), 흡입구 전                     | ✅ 컨텍스트 조건 |
| 4   | Sensed_Pt2          | Total pressure at fan inlet         | 팬 입구 총압 (전체 에너지 압력)                | ⭐⭐⭐⭐           |
| 5   | Sensed_TAT          | Total air temperature               | 총 공기 온도                                   | ⭐⭐⭐            |
| 6   | Sensed_WFuel        | Fuel flow rate                      | 연료 소비율 (kg/s 또는 lb/h)                   | ⭐⭐⭐⭐           |
| 7   | Sensed_VAFN         | Variable Area Fan Nozzle            | 팬 노즐 가변 밸브 위치 (%)                     | ⭐⭐             |
| 8   | Sensed_VBV          | Variable Bleed Valve                | 블리드 밸브 위치 (%)                           | ⭐⭐             |
| 9   | Sensed_Fan_Speed    | Nf – Fan speed                      | 팬 회전 속도 (저압 스풀 회전수)                | ⭐⭐⭐⭐           |
| 10  | Sensed_Core_Speed   | Nc – Core speed                     | 코어 회전 속도 (고압 스풀 RPM)                 | ⭐⭐⭐⭐⭐          |
| 11  | Sensed_T25          | T25 – LPC exit temperature          | 저압 압축기 후단 온도                           | ⭐⭐⭐⭐           |
| 12  | Sensed_T3           | T3 – HPC exit temperature           | 고압 압축기 후단 온도                           | ⭐⭐⭐⭐⭐          |
| 13  | Sensed_Ps3          | Static pressure at HPC exit         | HPC 출구 정압                                  | ⭐⭐⭐⭐           |
| 14  | Sensed_T45          | T45 – HPT exit temperature          | 고압 터빈 후단 온도                             | ⭐⭐⭐            |
| 15  | Sensed_P25          | Static pressure at LPC exit         | LPC 출구 정압                                  | ⭐⭐ (보조)       |
| 16  | Sensed_T5           | T5 – LPT exit temperature           | 저압 터빈 후단 온도                             | ⭐⭐ (보조)       |

---

## 📊 분류 기준 요약

| 범주           | 해당 센서 예시                   | 설명                              |
|----------------|----------------------------------|-----------------------------------|
| ✈️ 입력 조건   | Sensed_Altitude, Mach, Pamb      | 비행 상태 변수                   |
| 🔧 제어 변수   | VAFN, VBV                        | 밸브 제어 값                     |
| 🔄 회전계 지표 | Fan_Speed, Core_Speed            | RPM 기반 건강 진단                |
| 🌡 온도 센서   | TAT, T25, T3, T45, T5            | 고장 조짐 추적                    |
| 📈 압력 센서   | Pamb, Pt2, Ps3, P25              | 압축기/흡입구 상태 판단           |
| 🔥 연료 관련   | WFuel                            | 엔진 부하 및 연소 상태 지표       |

---

## 🔍 예측 모델 활용 팁

- **주요 Feature**: `T3`, `Ps3`, `Core_Speed`, `Fuel_Flow`
- **보조 Feature**: `P25`, `T5` (노이즈 또는 중복 가능)
- **운용 조건 보정**: `Altitude`, `Mach`, `Pamb` → 상태 분리 분석에 사용

---


# PHM 2025 메타데이터 컬럼 설명

이 문서는 PHM 2025 대회에서 제공되는 메타데이터 컬럼들의 의미와 분석 관점을 설명합니다. 메타데이터는 각 센서 데이터와 함께 제공되며, 엔진의 상태와 정비 이력 등을 반영합니다.

---

## 📦 메타데이터 컬럼 설명

| 컬럼명 | 의미 (영문) | 설명 (한글) | 활용도 |
|--------|-------------|-------------|--------|
| `ESN` | Engine Serial Number | 엔진 고유 식별자 (예: ESN101~ESN108) | 🔹 엔진 단위로 그룹 분석, 개별 고장 패턴 추적 |
| `Cycles_Since_New` | Cycles Since New | 해당 엔진이 출고된 후 수행한 누적 비행 횟수 | 🔹 RUL 예측 시 핵심 사용량 변수 |
| `Snapshot` | Snapshot ID | 하나의 비행 내 수집된 센서 데이터 시점 구분자 (1~8) | 🔹 비행 단계 구분 (이륙, 상승, 순항 등) |
| `Cumulative_WWs` | Cumulative Water Washes | 누적 워터워시 정비 횟수 (엔진 세척 이력) | 🔸 정비 이력 반영, 성능 회복 여부 분석 |
| `Cumulative_HPC_SVs` | Cumulative HPC Stator Vane Services | 누적 고압 압축기 스테이터 정비 횟수 | 🔸 압축기 성능 복구/유지 여부 평가 |
| `Cumulative_HPT_SVs` | Cumulative High-Pressure Turbine Services | 누적 고압 터빈 정비 횟수 | 🔸 고온 부품 마모 상태 및 회복 분석 지표 |

---

## 🧠 분석 관점 요약

### 🔸 `ESN`
- 개별 엔진 단위 분석 (groupby 처리)
- 엔진별로 성능 또는 고장 패턴 다를 수 있음

### 🔸 `Cycles_Since_New`
- 누적 사이클 수로 사용량 측정
- RUL(Remaining Useful Life) 계산에 직접 활용 가능:
  - `RUL = 최대 사이클 - 현재 사이클`

### 🔸 `Snapshot`
- 비행 한 회당 최대 8개 스냅샷
- 시점별 비교 분석: 상태 변화, 급변 패턴 확인

### 🔸 정비 이력 관련 변수
- `Cumulative_WWs`: 세척 정비 (엔진 성능 개선 목적)
- `Cumulative_HPC_SVs`: 고압 압축기 정적날개 정비
- `Cumulative_HPT_SVs`: 고압 터빈 부품 정비  
→ 정비 직후 성능 향상, 고장 지연 효과 여부 분석 가능

---

## 📊 예측 모델 활용 팁

| 변수 | 활용 방법 |
|------|-----------|
| `Cycles_Since_New` | RUL 예측의 독립 변수로 사용 |
| `Snapshot` | 단계별 상태 비교 또는 특정 시점 추출 (예: 순항 시만 사용) |
| `Cumulative_WWs`, `HPC_SVs`, `HPT_SVs` | 정비 이벤트 이후 성능 변화 패턴 감지 |
| `ESN` | 개별 엔진별 normalization 또는 one-hot encoding 처리 |

---
