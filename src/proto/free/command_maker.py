def create_command(gripper_id, function_reg, sub_function, rw, value):
    """
    공통 명령 프레임 생성 함수 (14바이트 포맷)
    """
    header = [0xFF, 0xFE, 0xFD, 0xFC]
    footer = [0xFB]
    reserve = 0x00
    data_bytes = list(value.to_bytes(4, byteorder='little', signed=True))
    return bytes(header + [gripper_id, function_reg, sub_function, rw, reserve] + data_bytes + footer)


def set_force(gripper_id=0x01, percent=50):
    """
    Force 설정 (20~100%)
    """
    if not 20 <= percent <= 100:
        raise ValueError("Force must be between 20 and 100%")
    return create_command(gripper_id, 0x05, 0x02, 0x01, percent)


def set_position(gripper_id=0x01, percent=100):
    """
    Position 설정 (0~100%)
    """
    if not 0 <= percent <= 100:
        raise ValueError("Position must be between 0 and 100%")
    return create_command(gripper_id, 0x06, 0x02, 0x01, percent)


def initialize(gripper_id=0x01):
    """
    그리퍼 초기화 명령
    """
    return create_command(gripper_id, 0x08, 0x02, 0x01, 0)


def set_feedback_enabled(gripper_id=0x01, enabled=True):
    """
    초기화 완료 시 피드백 활성화 여부 설정
    """
    value = 0xA5 if enabled else 0x00
    return create_command(gripper_id, 0x08, 0x01, 0x01, value)


def read_status(gripper_id=0x01):
    """
    그리퍼 상태 읽기 (움직임/파지 등)
    """
    return create_command(gripper_id, 0x0F, 0x01, 0x00, 0)


def parse_status_response(response_bytes):
    """
    상태 응답값 해석
    """
    if len(response_bytes) < 14:
        return "응답 부족"

    data = response_bytes[10:14]  # 11~14바이트가 상태값
    value = int.from_bytes(data, byteorder='little', signed=False)

    if value == 0x00:
        return "이동 중 or 대기"
    elif value == 0x02:
        return "위치 도달 (파지 실패)"
    elif value == 0x03:
        return "파지 성공 (위치 미도달)"
    else:
        return f"알 수 없는 상태: 0x{value:08X}"
