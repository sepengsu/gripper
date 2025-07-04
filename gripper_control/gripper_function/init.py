import time
from function_to_bytes.command_factory import (
    disable_io_mode,
    set_init_direction,
    initialize,
    read_init_state
)
from base_function.bus_io import send_and_receive, wait_until_initialized

def safe_initialize(client, slave_addr=0x01, direction=1, timeout=5.0) -> bool:
    """
    그리퍼를 안전하게 초기화합니다.
    순서: I/O OFF → 초기화 방향 설정 → 초기화 명령 → 완료 대기

    Args:
        client: ModbusSerialClient 객체
        slave_addr: 슬레이브 주소 (기본값 0x01)
        direction: 초기화 방향 (0=열기 기준, 1=닫기 기준)
        timeout: 초기화 완료까지 대기할 최대 시간 (초)

    Returns:
        bool: True면 성공, False면 실패 (Timeout)
    """
    print("🚦 Safe Initialize 시작")

    # 1. I/O 모드 비활성화
    send_and_receive(client, disable_io_mode(slave_addr), "Disable I/O Mode")

    # 2. 초기화 방향 설정
    send_and_receive(client, set_init_direction(slave_addr, direction), 
                     f"Set Init Direction ({'Close' if direction else 'Open'})")

    # 3. 초기화 명령
    send_and_receive(client, initialize(slave_addr), "Initialization Command")

    # 4. 초기화 완료 대기
    return wait_until_initialized(client, read_init_state(slave_addr), timeout)

# gripper_function/init.py

from function_to_bytes.command_factory import read_init_state
from function_to_bytes.response_parser import parse_init_state_response
from base_function.bus_io import read_and_describe

def is_initialized(client, slave_addr=0x01, timeout=1.0, interval=0.1) -> bool:
    """
    일정 시간 동안 InitState(0x0200)를 polling하여 초기화 완료 여부 확인

    Args:
        client: ModbusSerialClient
        slave_addr: 슬레이브 주소 (기본 0x01)
        timeout: 최대 대기 시간 (초)
        interval: polling 간격 (초)

    Returns:
        True → InitState == 1 (초기화 완료)
        False → 타임아웃까지 1이 안 나옴
    """
    print("🔍 초기화 상태 확인 중 (polling)...")
    start = time.time()

    while time.time() - start < timeout:
        result = read_and_describe(
            client,
            read_init_state(slave_addr),
            "Init State",
            parse_init_state_response,
            verbose=False
        )
        if result == "초기화 완료":
            print("✅ 초기화 상태 확인 완료 (InitState=1)")
            return True
        time.sleep(interval)

    print("⚠️ 초기화 상태가 감지되지 않음 (InitState=0)")
    return False
