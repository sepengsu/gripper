import time
from pymodbus.client import ModbusSerialClient
import serial
import sys
import os

connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if connection_path not in sys.path:
    sys.path.append(connection_path)
# 🔁 외부 함수들 import
from connect.connection import list_serial_ports, identify_gripper_port
from bus.function_to_bytes import create_modbus_read_command, parse_io_mode_response

def read_io_mode_state(client, slave_addr=0x01):
    """
    I/O 모드 상태를 읽고 출력
    """
    cmd = create_modbus_read_command(slave_addr, 0x0402, 1)
    client.socket.write(cmd)
    time.sleep(0.1)
    response = client.socket.read(7)

    print(f"📥 Raw Response: {response.hex().upper()}")
    value = parse_io_mode_response(response)

    if value == 1:
        print("⚠️ I/O 모드가 활성화되어 있습니다 (ON).")
    elif value == 0:
        print("✅ I/O 모드는 비활성화되어 있습니다 (OFF).")
    else:
        print(f"❓ 예상치 못한 값: {value}")

if __name__ == "__main__":
    ports = list_serial_ports()
    if not ports:
        print("❌ No serial ports found.")
    else:
        gripper_port = identify_gripper_port(ports)
        if gripper_port:
            client = ModbusSerialClient(
                port=gripper_port,
                baudrate=115200,
                stopbits=1,
                bytesize=8,
                parity='N',
                timeout=1
            )
            if client.connect():
                read_io_mode_state(client)
                client.close()
            else:
                print("❌ Failed to connect to gripper.")
        else:
            print("❌ Gripper not found.")
