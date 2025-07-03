# 흐름 순서 
# 1. Read_response 함수로 응답을 읽어와 유효한 프레임인지 검사
# 2. split_response 함수로 응답을 구조별로 분해
# 3. 응답 구조에서 필요한 값 추출
def read_response(ser, expected_length=14, timeout_sec=1.0):
    """
    그리퍼 응답을 수신하고, 유효한 프레임인지 검사하는 함수
    - ser: serial.Serial 객체
    - expected_length: 예상되는 응답 길이 (기본값 14바이트)
    - timeout_sec: 최대 대기 시간 (초)
    
    반환:
        - 유효한 14바이트 응답 (bytes)
    예외 발생:
        - Timeout 발생
        - 프레임 오류 발생
    """
    import time
    start_time = time.time()
    buffer = bytearray()

    while len(buffer) < expected_length:
        if ser.in_waiting > 0:
            buffer += ser.read(1)
        elif time.time() - start_time > timeout_sec:
            raise TimeoutError("응답 수신 시간 초과")
    
    # 1. 길이 체크
    if len(buffer) != expected_length:
        raise ValueError(f"응답 길이 오류: {len(buffer)}바이트 (기대값: {expected_length})")

    # 2. 헤더/엔드 바이트 확인
    if not (buffer[0:4] == b'\xFF\xFE\xFD\xFC' and buffer[-1] == 0xFB):
        raise ValueError("프레임 구조 오류: 시작/종료 바이트 불일치")

    return bytes(buffer)

def split_response(resp_bytes):
    """
    14바이트 응답 바이트를 구조별로 분해하여 dict 형태로 반환
    - resp_bytes: bytes (길이 14, 헤더와 종료 바이트 포함)

    반환 예시:
    {
        "gripper_id": 0x01,
        "function": 0x08,
        "sub_function": 0x02,
        "rw": 0x01,
        "reserve": 0x00,
        "data": 32비트 정수 (int),
        "raw_data_bytes": b'\x3C\x00\x00\x00'
    }
    """
    if len(resp_bytes) != 14:
        raise ValueError("응답 길이가 14바이트가 아닙니다.")
    
    # 구조 추출
    return {
        "gripper_id": resp_bytes[4],
        "function": resp_bytes[5],
        "sub_function": resp_bytes[6],
        "rw": resp_bytes[7],
        "reserve": resp_bytes[8],
        "raw_data_bytes": resp_bytes[9:13],
        "data": int.from_bytes(resp_bytes[9:13], byteorder='little', signed=True),
        "end": resp_bytes[13]
    }



