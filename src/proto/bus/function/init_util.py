from bus.function_to_bytes import (
    disable_io_mode,
    create_modbus_write_command,
    initialize,
    read_init_state,
)
import time

def safe_initialize(client, slave_addr=0x01, direction=1, timeout=5.0):
    """
    안전한 초기화를 수행하는 함수
    - direction: 0 = open 기준, 1 = close 기준 (기본값은 닫힘)
    - timeout: 초기화 완료 대기 최대 시간 (초)
    """
    def send_raw(cmd, label=""):
        client.socket.write(cmd)
        time.sleep(0.1)
        resp = client.socket.read(8)
        print(f"📤 Sent {label}: {cmd.hex().upper()}")
        print(f"📥 Response: {resp.hex().upper()}")
        return resp

    print("🚦 시작: Safe Initialization")

    # 1. I/O 모드 끄기
    send_raw(disable_io_mode(slave_addr), "Disable I/O Mode")

    # 2. 초기화 방향 설정
    send_raw(create_modbus_write_command(slave_addr, 0x0301, direction), f"Set Init Direction ({'Close' if direction == 1 else 'Open'})")

    # 3. 초기화 명령
    send_raw(initialize(slave_addr), "Initialization Command")

    # 4. 초기화 완료 대기
    print("⏳ Waiting for gripper to complete initialization...")
    cmd = read_init_state(slave_addr)
    start = time.time()
    while time.time() - start < timeout:
        client.socket.write(cmd)
        time.sleep(0.1)
        resp = client.socket.read(7)
        if len(resp) >= 5 and resp[1] == 0x03:
            value = int.from_bytes(resp[3:5], byteorder='big')
            if value == 1:
                print("✅ Initialization complete!")
                return True
    print("❌ Initialization timeout.")
    return False
