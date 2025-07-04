from gripper_control.function_to_bytes.command_factory import set_position, set_force
from gripper_control.base_function.bus_io import send_and_receive

def open_gripper(client, slave_addr=0x01, percent=0):
    """
    그리퍼를 엽니다 (0~100% 중 열리는 방향 기준).
    기본값은 완전히 열기 (0%)
    """
    permil = int(percent * 10)
    send_and_receive(client, set_position(slave_addr, permil), f"Open Gripper ({percent}%)")

def close_gripper(client, slave_addr=0x01, percent=100):
    """
    그리퍼를 닫습니다 (0~100% 중 닫히는 방향 기준).
    기본값은 완전히 닫기 (100%)
    """
    permil = int(percent * 10)
    send_and_receive(client, set_position(slave_addr, permil), f"Close Gripper ({percent}%)")

def move_to_position(client, permil=500, slave_addr=0x01):
    """
    그리퍼를 지정된 permil(0~1000) 위치로 이동시킵니다.
    """
    send_and_receive(client, set_position(slave_addr, permil), f"Move to {permil/10:.1f}% Position")

def set_force_level(client, percent=40, slave_addr=0x01):
    """
    파지 힘을 설정합니다 (20~100%)
    """
    send_and_receive(client, set_force(slave_addr, percent), f"Set Force {percent}%")
