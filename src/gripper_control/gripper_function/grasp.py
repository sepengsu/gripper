from function_to_bytes.command_factory import read_status
from base_function.bus_io import send_and_receive, read_and_describe
from gripper_function.motion import set_force_level, move_to_position
from function_to_bytes.response_parser import parse_status_response
import time

def grasp(client, slave_addr=0x01):
    """
    그리퍼를 파지 동작으로 움직입니다.
    Position이 작을수록 더 닫히며, Force를 강하게 설정합니다.
    """
    set_force_level(client, percent=20, slave_addr=slave_addr)        # 강한 힘
    move_to_position(client, permil=50, slave_addr=slave_addr)        # 거의 완전히 닫힘 (0~100 권장)

def ungrasp(client, slave_addr=0x01):
    """
    그리퍼를 엽니다.
    Position이 클수록 더 열리며, Force를 낮게 설정합니다.
    """
    set_force_level(client, percent=30, slave_addr=slave_addr)        # 약한 힘
    move_to_position(client, permil=900, slave_addr=slave_addr)       # 거의 완전히 열림 (800~1000 권장)

def safe_grasp(client, slave_addr=0x01, timeout=5.0, auto_release=False) -> bool:
    """
    개선된 파지 함수 - 충분한 상태 확인 후 성공 여부 판단
    """
    print("🦾 Grasp 시도 중...")
    grasp(client, slave_addr)

    start = time.time()
    no_object_count = 0
    success_count = 0

    while time.time() - start < timeout:
        result = read_and_describe(
            client,
            read_status(slave_addr),
            "Grasp Status",
            parse_status_response,
            verbose=False
        )

        if result == "파지 성공":
            success_count += 1
            if success_count >= 2:
                print("✅ 파지 성공 (안정적)")
                return True
        elif result == "위치 도달 (물체 없음)":
            no_object_count += 1
            if no_object_count >= 3:
                print("⚠️ 물체 없음 상태 지속 감지됨")
                break
        else:
            # 이동 중, 혹은 기타 응답 → 다시 대기
            pass

        time.sleep(0.2)

    print("❌ 파지 실패 또는 시간 초과")
    if auto_release:
        print("↩️ 자동으로 gripper 열기 수행...")
        ungrasp(client, slave_addr)

    return False

def grasp_and_wait(client, slave_addr=0x01, timeout=3.0) -> bool:
    """
    파지 후 상태가 '성공'일 때까지 기다립니다.
    """
    grasp(client, slave_addr)
    start = time.time()
    while time.time() - start < timeout:
        status = read_and_describe(client, read_status(slave_addr), "Grasp Status", parse_status_response, verbose=False)
        if status == "파지 성공":
            print("✅ 파지 성공")
            return True
        time.sleep(0.1)
    print("❌ 파지 실패 또는 시간 초과")
    return False

def is_grasp_success(resp_bytes: bytes) -> bool:
    """
    상태 응답에서 파지 성공인지 검사합니다.
    """
    if len(resp_bytes) >= 5 and resp_bytes[1] == 0x03:
        return int.from_bytes(resp_bytes[3:5], byteorder='big') == 2
    return False
