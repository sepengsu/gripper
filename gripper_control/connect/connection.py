import serial.tools.list_ports
from pymodbus.client.serial import ModbusSerialClient  # 최신 구조

def list_serial_ports():
    """
    현재 시스템에 연결된 시리얼 포트 리스트 반환
    ex) ['COM3', 'COM4'] 또는 ['/dev/ttyUSB0', '/dev/ttyUSB1']
    """
    ports = serial.tools.list_ports.comports()
    port_names = [p.device for p in ports]
    # print(f"🔌 Found ports: {port_names}")
    return port_names

def identify_gripper_port(port_list):
    """
    주어진 포트 리스트 중 실제 gripper가 연결된 포트 식별
    Modbus RTU 프로토콜로 응답 확인
    """
    for port in port_list:
        # print(f"🔍 Testing port: {port}")
        try:
            client = ModbusSerialClient(
                port=port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )

            if client.connect():
                result = client.read_holding_registers(address=0x0200, count=1, slave=1)  # unit=1 → slave=1
                client.close()
                if result and not result.isError():
                    print(f"✅ Gripper found at {port} (InitState={result.registers[0]})")
                    return port
                else:
                    print(f"⚠️ No valid response on {port}")
            else:
                pass
                # print(f"❌ Failed to connect to {port}")
        except Exception as e:
            pass
            # print(f"⚠️ Error on {port}: {e}")
    print("❌ Gripper not found in the given ports.")
    return None

if __name__ == "__main__":
    ports = list_serial_ports()

    if not ports:
        print("❌ No serial ports found.")
    else:
        gripper_port = identify_gripper_port(ports)
        if gripper_port:
            print(f"Gripper is connected to: {gripper_port}")
        else:
            print("No gripper detected on available ports.")
