import time
from function_to_bytes.response_parser import parse_modbus_exception_response

def send_and_receive(client, cmd_bytes: bytes, label: str = "") -> bytes:
    """
    명령을 전송하고 응답을 수신하며 해석 결과를 출력합니다.
    """
    client.socket.write(cmd_bytes)
    print(f"📤 Sent {label} command: {cmd_bytes.hex().upper()}")
    time.sleep(0.1)
    response = client.socket.read(8)
    print(f"📥 {label} Response: {response.hex().upper()}")

    parsed = parse_modbus_exception_response(response)
    if isinstance(parsed, dict):
        print(f"🔍 {label} Exception → Func: 0x{parsed['original_function']:02X}, Code: 0x{parsed['exception_code']:02X} ({parsed['meaning']})")
    else:
        print(f"🔍 {label} Status: {parsed}")
    return response

def wait_until_initialized(client, read_init_state_cmd: bytes, timeout: float = 5.0) -> bool:
    """
    초기화가 완료될 때까지 대기합니다.
    """
    print("⏳ Waiting for gripper initialization to complete...")
    start = time.time()
    while time.time() - start < timeout:
        client.socket.write(read_init_state_cmd)
        time.sleep(0.1)
        resp = client.socket.read(7)
        if len(resp) >= 5 and resp[1] == 0x03:
            val = int.from_bytes(resp[3:5], byteorder='big')
            if val == 1:
                print("✅ Gripper is initialized.")
                return True
    print("❌ Initialization timeout.")
    return False

def read_and_parse_status(client, read_status_cmd: bytes, parser_func, label: str = "Status") -> str:
    """
    상태를 읽고 파싱하여 반환합니다.
    """
    client.socket.write(read_status_cmd)
    time.sleep(0.1)
    resp = client.socket.read(7)
    status = parser_func(resp)
    print(f"📊 {label}: {status}")
    return status

def read_and_describe(client, cmd_bytes: bytes, label: str, parser_func, verbose=True) -> str:
    """
    Modbus 명령을 보내고 응답을 받아 파싱하여 한글로 출력합니다.
    
    Args:
        client: ModbusSerialClient
        cmd_bytes: 전송할 명령 바이트
        label: 로그용 레이블 (예: '그리퍼 상태')
        parser_func: 응답 파싱 함수 (예: parse_status_response)
        verbose: True일 경우 로그 출력

    Returns:
        str: 해석된 결과 문자열 (한글 포함)
    """
    client.socket.write(cmd_bytes)
    time.sleep(0.1)
    resp = client.socket.read(7)

    if verbose:
        print(f"📤 Sent {label} command: {cmd_bytes.hex().upper()}")
        print(f"📥 {label} Response: {resp.hex().upper()}")

    result = parser_func(resp)

    if verbose:
        print(f"📝 {label} 결과 → {result}")
    return result
