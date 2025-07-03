import struct

def calc_crc(data):
    """
    CRC-16 계산 (Modbus RTU 표준, low byte 먼저)
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            lsb = crc & 0x0001
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return struct.pack('<H', crc)  # little-endian (Low byte first)

def create_modbus_write_command(slave_addr, reg_addr, value):
    """
    단일 레지스터 쓰기 명령 생성 (Function Code 0x06)
    """
    frame = bytearray()
    frame.append(slave_addr)
    frame.append(0x06)  # Function code: Write Single Register
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += value.to_bytes(2, byteorder='big')
    frame += calc_crc(frame)
    return bytes(frame)

def create_modbus_read_command(slave_addr, reg_addr, count=1):
    """
    연속 레지스터 읽기 명령 생성 (Function Code 0x03)
    """
    frame = bytearray()
    frame.append(slave_addr)
    frame.append(0x03)  # Function code: Read Holding Register
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += count.to_bytes(2, byteorder='big')
    frame += calc_crc(frame)
    return bytes(frame)

# === 명령 함수 ===

def initialize(slave_addr=0x01):
    return create_modbus_write_command(slave_addr, 0x0100, 0xA5)

def set_force(slave_addr=0x01, percent=50):
    if not 20 <= percent <= 100:
        raise ValueError("Force must be between 20 and 100")
    return create_modbus_write_command(slave_addr, 0x0101, percent)

def set_position(slave_addr=0x01, permil=500):
    if not 0 <= permil <= 1000:
        raise ValueError("Position must be between 0 and 1000 (permil)")
    return create_modbus_write_command(slave_addr, 0x0103, permil)

def read_status(slave_addr=0x01):
    return create_modbus_read_command(slave_addr, 0x0201, 1)

def read_position(slave_addr=0x01):
    return create_modbus_read_command(slave_addr, 0x0202, 1)

def read_init_state(slave_addr=0x01):
    return create_modbus_read_command(slave_addr, 0x0200, 1)

# === 상태 응답 파서 ===

def parse_status_response(response):
    """
    Modbus RTU 상태 응답 파싱 (예: 01 03 02 00 02 CRC...)
    """
    if len(response) < 5 or response[1] != 0x03:
        return "유효하지 않은 응답"

    status = int.from_bytes(response[3:5], byteorder='big')
    if status == 0:
        return "이동 중"
    elif status == 1:
        return "위치 도달 (물체 없음)"
    elif status == 2:
        return "파지 성공"
    elif status == 3:
        return "물체 낙하"
    else:
        return f"알 수 없는 상태값: {status}"
