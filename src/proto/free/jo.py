import serial
import time

# 포트 설정
ser = serial.Serial("COM6", baudrate=115200, timeout=2)

### 1. (선택) 초기화 피드백 설정 명령
# 설명: 초기화 완료 후 자동으로 응답하게 설정할 수 있음
# 이 단계는 생략해도 동작은 가능하지만, 피드백 받기를 원하면 활성화 추천
set_feedback_cmd = bytes.fromhex("FFFEFDFC01080101000000000000FB")
ser.write(set_feedback_cmd)
resp1 = ser.read(14)
print("초기화 피드백 설정 응답:", resp1.hex())

### 2. 초기화 실행 명령
init_cmd = bytes.fromhex("FFFEFDFC01080201000000000000FB")
ser.write(init_cmd)
resp2 = ser.read(14)
print("초기화 실행 응답:", resp2.hex())

### 3. 초기화 대기 (1~2초 정도)
time.sleep(2)

### 4. 초기화 상태 읽기
check_cmd = bytes.fromhex("FFFEFDFC01080200000000000000FB")
ser.write(check_cmd)
resp3 = ser.read(14)
print("초기화 상태 응답:", resp3.hex())

# 상태 값 분석
status_data = resp3[10:14]
if status_data == b'\x01\x00\x00\x00':
    print("✅ 초기화 완료됨!")
elif status_data == b'\x00\x00\x00\x00':
    print("⌛ 아직 초기화되지 않음")
else:
    print("❓ 알 수 없는 응답 값:", status_data.hex())

ser.close()
