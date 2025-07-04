import sys
import os
import time
from pymodbus.client import ModbusSerialClient

# === 경로 설정 ===
gripper_control_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if gripper_control_path not in sys.path:
    sys.path.append(gripper_control_path)

# === 모듈 import ===
from connect.connection import list_serial_ports, identify_gripper_port
from gripper_function.init import safe_initialize, is_initialized
from gripper_function.basic_motion import close, open  # ✅ open/close 모듈 import

# === 메인 실행 ===
if __name__ == "__main__":
    ports = list_serial_ports()
    if not ports:
        print("❌ No serial ports found.")
        sys.exit(1)

    gripper_port = identify_gripper_port(ports)
    if not gripper_port:
        print("❌ No gripper detected.")
        sys.exit(1)

    print(f"✅ Gripper is connected to: {gripper_port}")

    client = ModbusSerialClient(
        port=gripper_port,
        baudrate=115200,
        stopbits=1,
        bytesize=8,
        parity='N',
        timeout=1
    )

    if not client.connect():
        print("❌ Failed to connect to gripper.")
        sys.exit(1)

    print("🔌 Connected via Modbus RTU")

    # ✅ Init 상태 확인 및 필요 시 초기화
    if is_initialized(client):
        print("✅ 이미 초기화 상태입니다. safe_initialize 생략.")
    else:
        if not safe_initialize(client, direction=1):
            print("🛑 Initialization failed.")
            client.close()
            sys.exit(1)
        print("⚙️ Gripper initialized")

    # === 열고 닫기 반복 3회 ===
    for i in range(3):
        print(f"\n🔁 Cycle {i+1} - Closing gripper...")
        close(client, force=70, permil=850)

        time.sleep(1.5)

        print("🔁 Opening gripper...")
        open(client, force=30, permil=100)

        time.sleep(1.0)
        
    close(client, force=70, permil=100)
    time.sleep(1.5)
    client.close()
    print("\n🔚 Open-Close sequence finished.")
