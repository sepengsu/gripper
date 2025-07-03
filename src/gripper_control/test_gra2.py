import sys
import os
import time
from pymodbus.client import ModbusSerialClient

# === gripper_control 경로 설정 ===
gripper_control_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if gripper_control_path not in sys.path:
    sys.path.append(gripper_control_path)

# === 모듈 import ===
from connect.connection import list_serial_ports, identify_gripper_port
from gripper_function.init import safe_initialize
from gripper_function.grasp import safe_grasp, ungrasp
from function_to_bytes.command_factory import read_init_state
from function_to_bytes.response_parser import parse_init_state_response
from base_function.bus_io import read_and_describe

# === 실행 ===
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

    # ✅ Init 상태 먼저 확인
    init_state = read_and_describe(
        client,
        read_init_state(slave_addr=0x01),
        "Init State",
        parse_init_state_response
    )

    if init_state == "초기화 완료":
        print("✅ 이미 초기화 상태입니다. safe_initialize 생략.")
    else:
        if not safe_initialize(client, direction=1):
            print("🛑 Initialization failed.")
            client.close()
            sys.exit(1)
        print("⚙️ Gripper initialized")

    # 👉 안전 파지 시도
    ungrasp(client)
    if safe_grasp(client, timeout=10.0, auto_release=False):
        print("⏳ Holding object for 5 seconds...")
        time.sleep(5)

        # 👉 수동 해제
        ungrasp(client)
        print("✅ Grasp-ungrasp cycle complete")
    else:
        print("🛑 Grasp failed. Object may not be present.")

    client.close()
