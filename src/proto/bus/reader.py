import time
import struct

def read_modbus_response(ser, expected_length=8, timeout_sec=1.0):
    """
    Modbus RTU 응답을 시리얼에서 읽고 CRC 검증까지 수행
    - ser: serial.Serial 또는 socket 유사 객체
    - expected_length: 기본 8바이트 (0x06 응답 기준)
    """
    buffer = bytearray()
    start_time = time.time()

    while len(buffer) < expected_length:
        if ser.in_waiting > 0:
            buffer += ser.read(1)
        elif time.time() - start_time > timeout_sec:
            raise TimeoutError("응답 수신 시간 초과")

    if len(buffer) != expected_length:
        raise ValueError(f"응답 길이 오류: {len(buffer)}바이트 (기대: {expected_length})")

    # CRC 검증
    data, crc_recv = buffer[:-2], buffer[-2:]
    crc_calc = calc_crc(data)

    if crc_recv != crc_calc:
        raise ValueError(f"CRC 불일치 (받은값: {crc_recv.hex()} / 계산값: {crc_calc.hex()})")

    return bytes(buffer)

def split_modbus_response(resp_bytes):
    """
    Modbus RTU 응답 바이트를 구조별 dict로 분해
    """
    if len(resp_bytes) != 8:
        raise ValueError("Modbus 응답 길이는 8바이트여야 합니다.")

    return {
        "slave_id": resp_bytes[0],
        "function": resp_bytes[1],
        "register": (resp_bytes[2] << 8) | resp_bytes[3],
        "value": (resp_bytes[4] << 8) | resp_bytes[5],
        "crc": resp_bytes[6:8]
    }

def calc_crc(data):
    """
    Modbus RTU CRC-16 계산 함수 (Little Endian)
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

def parse_modbus_exception_response(resp_bytes):
    """
    Modbus 예외 응답 파서
    예: 01 86 04 CRC1 CRC2
    - 0x86 = 원래 0x06 명령에서 오류 (0x80 더해짐)
    - 0x04 = 예외 코드 (Slave Device Failure)

    반환:
        dict 또는 에러 메시지 문자열
    """
    if len(resp_bytes) < 5:
        return "❌ 응답 길이 부족 (예외 응답 아님)"
    
    slave_id = resp_bytes[0]
    function_code = resp_bytes[1]
    exception_code = resp_bytes[2]

    if function_code < 0x80:
        return "✅ 정상 응답 (예외 아님)"

    code_meaning = {
        0x01: "Illegal Function",
        0x02: "Illegal Data Address",
        0x03: "Illegal Data Value",
        0x04: "Slave Device Failure",
        0x06: "Slave Device Busy",
    }

    return {
        "slave_id": slave_id,
        "original_function": function_code - 0x80,
        "exception_code": exception_code,
        "meaning": code_meaning.get(exception_code, "Unknown Error Code")
    }
