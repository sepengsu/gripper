# 🔍 AG 시리즈 그리퍼 통신 방식 분석 및 선택 가이드

## 1. 통신 방식 개요

AG 시리즈 그리퍼(DH-Robotics)는 다음 두 가지 주요 통신 방식을 지원합니다:

| 통신 방식 | 설명 | 특징 |
|-----------|------|------|
| **Modbus RTU** | 산업 표준 시리얼 통신 프로토콜 | ✅ 표준화 / 범용성 / 다양한 라이브러리 지원 |
| **Free Protocol (RS485)** | DH-Robotics 고유의 바이너리 프레임 기반 프로토콜 | ⚠️ 직접 프레임 구성 필요 / 비표준 방식 |

---

## 2. Free Protocol vs. Modbus RTU 차이점

| 항목 | Modbus RTU | Free Protocol (RS485) |
|------|-------------|------------------------|
| 프레임 구조 | 표준 Modbus RTU 프레임 (주소 + 기능 + 데이터 + CRC) | 커스텀 14바이트 바이너리 구조 |
| 파이썬 지원 | ✅ `pymodbus` 등 풍부한 라이브러리 | ❌ 수동 구현 필요 (`struct`, `serial` 직접 사용) |
| 명령어 이해도 | 고수준 (레지스터 기반 제어) | 저수준 (기계어 수준 바이트 처리) |
| 디버깅 용이성 | 쉬움 (에러 해석 가능) | 어려움 (프레임 해석 복잡) |
| 권장 상황 | 프로그래밍 직접 제어 시 | 내장형 장치에서 미리 정의된 시퀀스 실행 시 |

---

## 3. 현재 연결 방식 분석

| 항목 | 내용 |
|------|------|
| 사용 중인 포트 | **Micro USB (`Debug`)** |
| 내부 기능 | USB-to-RS485 변환, 가상 COM 포트로 인식 |
| 운영체제 인식 | **STMicroelectronics Virtual COM Port** (Windows 장치 관리자에서 확인 가능) |
| 사용 가능한 프로토콜 | **Modbus RTU 전용 통신만 지원됨** |
| 참고사항 | Free Protocol은 RS485 직결(터미널 블록) 방식이어야 사용 가능하며, USB Debug 포트에서는 사용 불가 |

---

## 4. 어떤 프로토콜을 사용해야 할까?

| 조건 | 선택 |
|------|------|
| Python으로 직접 통신하고 싶음 | ✅ Modbus RTU |
| 외부 프로그램 없이 제어하고 싶음 | ✅ Modbus RTU |
| 현재 USB로 연결하여 제어하려 함 | ✅ Modbus RTU (USB 포트는 Modbus 전용 시리얼 장치임) |
| RS485 단자 직접 연결 가능함 | ⚠️ Free Protocol 가능 (단, 프레임 수동 구성 필요) |

---

## ✅ 결론

> **현재 Micro USB (Debug) 포트를 통해 연결된 상황에서는 반드시 `Modbus RTU` 방식으로 통신해야 하며, 이는 Python에서도 `pymodbus` 라이브러리를 통해 쉽게 구현 가능합니다.**

---

## 📌 추천 라이브러리 및 설정 요약

- **라이브러리**: `pymodbus`
- **포트**: `COMx` (Windows) / `/dev/ttyUSBx` (Linux)
- **Baudrate**: 115200
- **Parity**: None
- **Stopbit**: 1
- **Slave ID**: 1

### ▶️ 예제 코드

```python
from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    port='COM5',         # 실제 환경에 맞게 수정
    baudrate=115200,
    stopbits=1,
    bytesize=8,
    parity='N',
    timeout=1
)

client.connect()

# 초기화 명령
client.write_register(address=0x0100, value=0xA5, unit=1)

# 상태 확인
res = client.read_holding_registers(address=0x0201, count=1, unit=1)
print("Gripper State:", res.registers[0])

client.close()
