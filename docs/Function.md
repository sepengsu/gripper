# 함수 지정 

위 문서는 함수를 어떻게 지정했는지와 사용법을 설명합니다. 

## 1. 주요 함수 사용법 요약

| 기능 | 함수 이름 | 설명 | 사용 예시 (gripper_id=1) |
|------|-----------|------|---------------------------|
| 초기화 | `initialize()` | 그리퍼를 초기화합니다. 전원 켜고 반드시 한 번 호출해야 합니다. | `cmd = initialize()` |
| 파지 힘 설정 | `set_force(percent)` | 파지 힘을 20~100% 사이로 설정합니다. | `cmd = set_force(1, 60)` |
| 위치 설정 | `set_position(percent)` | 그리퍼의 열림/닫힘 정도를 0~100%로 설정합니다. | `cmd = set_position(1, 80)` |
| 상태 확인 | `read_status()` | 현재 그리퍼의 상태를 읽는 명령입니다. | `cmd = read_status(1)` |
| 상태 파싱 | `parse_status_response()` | 응답된 바이트값을 해석해 의미를 알려줍니다. | `parse_status_response(response)` |
| 피드백 설정 | `set_feedback_enabled(enabled=True)` | 초기화 후 피드백을 받을지 여부를 설정합니다. | `cmd = set_feedback_enabled(1, True)` |
