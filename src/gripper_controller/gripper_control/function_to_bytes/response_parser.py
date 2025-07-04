def parse_status_response(resp_bytes: bytes) -> str:
    """
    상태 응답 파싱 (예: 01 03 02 00 02 CRC1 CRC2)
    """
    if len(resp_bytes) < 5 or resp_bytes[1] != 0x03:
        return "⚠️ 유효하지 않은 응답"

    value = int.from_bytes(resp_bytes[3:5], byteorder='big')
    status_map = {
        0: "이동 중",
        1: "위치 도달 (물체 없음)",
        2: "파지 성공",
        3: "물체 낙하",
    }
    return status_map.get(value, f"알 수 없는 상태값: {value}")

def parse_io_mode_response(resp_bytes: bytes) -> str:
    """
    I/O 모드 상태 응답 파싱 (예: 01 03 02 00 01 CRC1 CRC2)
    :return: 'ON' 또는 'OFF' 또는 오류 메시지
    """
    if len(resp_bytes) < 7:
        return "⚠️ 응답 길이 부족"
    if resp_bytes[1] != 0x03:
        return "⚠️ Function Code 불일치"

    value = int.from_bytes(resp_bytes[3:5], byteorder='big')
    return "ON" if value else "OFF"

def parse_modbus_exception_response(resp_bytes: bytes):
    """
    예외 응답 여부 확인 및 해석
    예: 01 86 04 CRC1 CRC2 → 0x86 = 0x06 | 0x80 (예외 응답), 0x04 = exception code
    :return: dict 또는 '정상 응답'
    """
    if len(resp_bytes) >= 3 and (resp_bytes[1] & 0x80):
        original_func = resp_bytes[1] & 0x7F
        exc_code = resp_bytes[2]
        meaning = {
            0x01: "Illegal Function",
            0x02: "Illegal Data Address",
            0x03: "Illegal Data Value",
            0x04: "Slave Device Failure",
            0x05: "Acknowledge",
            0x06: "Slave Device Busy",
            0x08: "Memory Parity Error",
        }.get(exc_code, "Unknown Error Code")

        return {
            "original_function": original_func,
            "exception_code": exc_code,
            "meaning": meaning
        }
    return "✅ 정상 응답 (예외 아님)"

def parse_init_state_response(response):
    """
    0x0200 응답값 해석 (InitState)
    0 → 초기화 안됨
    1 → 초기화 완료
    """
    if len(response) < 5 or response[1] != 0x03:
        return "유효하지 않은 응답"
    value = int.from_bytes(response[3:5], "big")
    return "초기화 완료" if value == 1 else "초기화 안됨"
