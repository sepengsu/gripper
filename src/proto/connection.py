import platform
import serial.tools.list_ports
from pymodbus.client import ModbusSerialClient

def list_serial_ports():
    """
    현재 시스템에 연결된 시리얼 포트 리스트 반환
    ex) ['COM3', 'COM4'] 또는 ['/dev/ttyUSB0', '/dev/ttyUSB1']
    """
    ports = serial.tools.list_ports.comports()
    port_names = [p.device for p in ports]
    print(f"🔌 Found ports: {port_names}")
    return port_names

def identify_gripper_port(port_list):
    """
    주어진 포트 리스트 중 실제 gripper가 연결된 포트 식별
    Modbus RTU 프로토콜로 응답 확인
    """
    for port in port_list:
        print(f"🔍 Testing port: {port}")
        try:
            client = ModbusSerialClient(
                method='rtu',
                port=port,
                baudrate=115200,
                stopbits=1,
                bytesize=8,
                parity='N',
                timeout=0.5
            )
            if client.connect():
                result = client.read_holding_registers(address=0x0200, count=1, unit=1)  # Init state
                client.close()
                if result and not result.isError():
                    print(f"✅ Gripper found at {port} (InitState={result.registers[0]})")
                    return port
        except Exception as e:
            print(f"⚠️ Error on {port}: {e}")
    print("❌ Gripper not found in the given ports.")
    return None
