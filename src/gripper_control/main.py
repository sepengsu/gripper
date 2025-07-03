import serial
import sys
import os

connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if connection_path not in sys.path:
    sys.path.append(connection_path)
import time
from connect.connection import list_serial_ports, identify_gripper_port  # 함수 불러오기
from bus.function_to_bytes import initialize  # 함수 정의한 파일명에 맞게 import
from pymodbus.client import ModbusSerialClient

if __name__ == "__main__":
    ports = list_serial_ports()

    if not ports:
        print("❌ No serial ports found.")
    else:
        gripper_port = identify_gripper_port(ports)
        if gripper_port:
            print(f"✅ Gripper is connected to: {gripper_port}")

            # 📡 Modbus RTU 클라이언트 생성
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

                # ✉️ Initialization 명령 전송
                init_cmd = initialize(slave_addr=0x01)
                client.socket.write(init_cmd)  # 직접 write (pymodbus로는 커스텀 프레임 직접 전송 필요)
                print(f"📤 Sent initialization command: {init_cmd.hex().upper()}")

                # ⏱ 응답 대기
                time.sleep(0.1)
                response = client.socket.read(8)  # 응답 프레임 수동으로 읽기 (일반적으로 8~9바이트)
                print(f"📥 Response: {response.hex().upper()}")

                client.close()
            else:
                print("❌ Failed to connect via Modbus RTU.")
        else:
            print("❌ No gripper detected on available ports.")
