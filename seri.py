import serial
import time

# COM 포트 열기
ser = serial.Serial("COM6", baudrate=115200, timeout=1)

# 초기화 명령 (ID = 1 기준)
init_cmd = bytes.fromhex("FFFEFDFC01080201000000000000FB")

# 전송
ser.write(init_cmd)

# 응답 수신
response = ser.read(14)
print("✅ 응답:", response.hex())

# 응답 분석 (성공 시 동일한 명령을 되돌림)
if response[:4] == b'\xFF\xFE\xFD\xFC':
    print("✅ 초기화 명령 정상 수신됨 (Gripper가 반응함)")
else:
    print("❌ 응답 없음 또는 실패")

ser.close()
