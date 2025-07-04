import sys
import os
import time
from pymodbus.client import ModbusSerialClient

# === 경로 설정 ===
connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if connection_path not in sys.path:
    sys.path.append(connection_path)

# === 모듈 import ===
from connect.connection import list_serial_ports, identify_gripper_port
from function_to_bytes.command_factory import set_force, set_position
from base_function.bus_io import send_and_receive
from gripper_function.init import safe_initialize
from gripper_function.motion import move_to_position, set_force_level

# === 메인 실행 ===
if __name__ == "__main__":
    ports = list_serial_ports()

    if not ports:
        print("❌ No serial ports found.")
        sys.exit(1)

    gripper_port = identify_gripper_port(ports)
    if not gripper_port:
        print("❌ No gripper detected on available ports.")
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
        print("❌ Failed to connect via Modbus RTU.")
        sys.exit(1)

    print("🔌 Connected to gripper via Modbus RTU")

    # ✅ 안전 초기화 (기본 방향: 닫힘)
    if safe_initialize(client, direction=1):
        # ✅ Force & Position 설정
        set_force_level(client, percent=40)           # 40% 힘
        move_to_position(client, permil=200)          # 20% 위치 (permil=200)
    else:
        print("🛑 Initialization failed. Aborting.")

    client.close()
