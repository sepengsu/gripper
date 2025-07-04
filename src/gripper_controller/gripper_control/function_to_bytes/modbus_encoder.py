import struct

def calc_crc(data: bytes) -> bytes:
    """
    CRC-16 계산 (Modbus RTU 표준, low byte 먼저)
    :param data: 바이트열 (CRC를 제외한 부분)
    :return: CRC 바이트 (2바이트, little-endian)
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

def create_modbus_write_command(slave_addr: int, reg_addr: int, value: int) -> bytes:
    """
    Function code 0x06 - Write Single Register
    :param slave_addr: 슬레이브 주소
    :param reg_addr: 레지스터 주소
    :param value: 쓸 값 (16bit)
    :return: 전송할 바이트열
    """
    frame = bytearray()
    frame.append(slave_addr)
    frame.append(0x06)  # Write Single Register
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += value.to_bytes(2, byteorder='big')
    frame += calc_crc(frame)
    return bytes(frame)

def create_modbus_read_command(slave_addr: int, reg_addr: int, count: int = 1) -> bytes:
    """
    Function code 0x03 - Read Holding Registers
    :param slave_addr: 슬레이브 주소
    :param reg_addr: 시작 레지스터 주소
    :param count: 읽을 레지스터 개수
    :return: 전송할 바이트열
    """
    frame = bytearray()
    frame.append(slave_addr)
    frame.append(0x03)  # Read Holding Registers
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += count.to_bytes(2, byteorder='big')
    frame += calc_crc(frame)
    return bytes(frame)
