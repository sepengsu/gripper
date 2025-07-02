# 🤖 M2E-B1-1 그리퍼 제어 프로젝트

Python 3.10으로 **Windows에서 개발하고**, **Ubuntu 22.04에서 수정 및 실행** 가능한 **산업용 그리퍼 제어 프로그램**입니다.
**RS-485 통신**을 기반으로 하며, 대상 모델은 **M2E-B1-1**입니다.

---

## 📦 사용 기술

| 분류          | 사용 도구 / 패키지                                             | 아이콘   |
| ----------- | ------------------------------------------------------- | ----- |
| 언어          | Python 3.10                                             | 🐍    |
| 통신 방식       | RS-485 + [PySerial](https://pythonhosted.org/pyserial/) | 🔌    |
| 가상환경        | `venv`                                                  | 🧪    |
| 운영체제        | Windows 10 이상 / Ubuntu 22.04                            | 🪟 🐧 |
| 하드웨어        | 그리퍼: M2E-B1-1                                           | 🤲    |
| 전원공급기(SMPS) | LRS-350-24 (24V / 최대 14.6A)                             | ⚡     |

---

## 🔧 시스템 개요

* **그리퍼 모델:** M2E-B1-1 (24VDC, 0.1A)
* **전원:** LRS-350-24 SMPS (24V, 최대 14.6A)
* **통신 방식:** RS-485 (USB-시리얼 어댑터 활용)
* **프로토콜:** DH (제조사 커스텀)
* **목적:** 그리퍼 제어 및 피드백 수신

---

## 🧑‍💻 개발 환경 설정

### ✅ Windows (개발 환경)

1. **Python 3.10 설치**

   * [python.org](https://www.python.org/downloads/release/python-3100/)에서 다운로드

2. **가상 환경 생성 및 실행**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **필수 패키지 설치**

   ```bash
   pip install pyserial
   ```

4. **프로그램 실행**

   ```bash
   python main.py
   ```

---

### 🐧 Ubuntu 22.04 (수정 및 실행 환경)

1. **Python 3.10 설치**

   ```bash
   sudo apt update
   sudo apt install python3.10 python3.10-venv
   ```

2. **프로젝트 클론 및 가상 환경 구성**

   ```bash
   git clone <your-repo-url>
   cd <project-dir>
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. **필수 패키지 설치**

   ```bash
   pip install pyserial
   ```

4. **시리얼 포트 권한 설정**

   ```bash
   sudo usermod -a -G dialout $USER
   sudo chmod 666 /dev/ttyUSB0  # 사용 중인 포트로 수정
   ```

5. **프로그램 실행**

   ```bash
   python main.py
   ```

---

## 🔌 RS-485 배선도

| 신호  | 연결 대상      |
| --- | ---------- |
| 24V | SMPS + 단자  |
| GND | SMPS - 단자  |
| A   | RS-485 A 선 |
| B   | RS-485 B 선 |

> ⚠️ **주의:** 산업 환경 또는 장거리 사용 시 종단 저항 및 절연 회로 권장

---

## 📁 프로젝트 구조

```
gripper-control/
├── README.md
├── main.py
├── serial_handler.py
├── gripper_protocol.py
├── requirements.txt
└── venv/
```

---

## ✅ 개발 체크리스트

* [] Windows용 Python 3.10 개발 완료
* [] RS-485 통신 정상 동작 확인
* [] M2E-B1-1 명령어 구현 완료
* [] Ubuntu 환경 호환 테스트
* [ ] GUI 또는 피드백 시각화 기능 추가 예정

