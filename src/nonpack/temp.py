import serial
import sys
import os
import time
from pymodbus.client import ModbusSerialClient

# === 경로 설정 ===
connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if connection_path not in sys.path:
    sys.path.append(connection_path)

# === 필요한 함수 import ===
from connect.connection import list_serial_ports, identify_gripper_port
from bus.function_to_bytes import (
    set_force,
    set_position,
)
from bus.reader import parse_modbus_exception_response
from bus.function.init_util import safe_initialize  # ✅ 새로 만든 함수 import

# === 전송 함수 정의 ===
def send_and_receive(client, cmd_bytes, label=""):
    client.socket.write(cmd_bytes)
    print(f"📤 Sent {label} command: {cmd_bytes.hex().upper()}")
    time.sleep(0.1)
    response = client.socket.read(8)
    print(f"📥 {label} Response: {response.hex().upper()}")

    # 예외 응답 해석 추가
    parsed = parse_modbus_exception_response(response)
    if isinstance(parsed, dict):
        print(f"🔍 {label} Exception Info → Function: 0x{parsed['original_function']:02X}, Code: 0x{parsed['exception_code']:02X} ({parsed['meaning']})")
    else:
        print(f"🔍 {label} 상태: {parsed}")
    return response

# === 메인 실행 ===
if __name__ == "__main__":
    ports = list_serial_ports()

    if not ports:
        print("❌ No serial ports found.")
    else:
        gripper_port = identify_gripper_port(ports)
        if gripper_port:
            print(f"✅ Gripper is connected to: {gripper_port}")

            client = ModbusSerialClient(
                port=gripper_port,
                baudrate=115200,
                stopbits=1,
                bytesize=8,
                parity='N',
                timeout=1
            )

            if client.connect():
                print("🔌 Connected to gripper via Modbus RTU")

                # ✅ 안전 초기화 (기본: 닫힘 방향)
                if safe_initialize(client, direction=1):
                    # ✅ 초기화 성공 시 Force & Position 전송
                    send_and_receive(client, set_force(0x01, 40), "Set Force 40%")
                    send_and_receive(client, set_position(0x01, 200), "Move to Position 50%")
                else:
                    print("🛑 Initialization failed. Aborting.")

                client.close()
            else:
                print("❌ Failed to connect via Modbus RTU.")
        else:
            print("❌ No gripper detected on available ports.")
