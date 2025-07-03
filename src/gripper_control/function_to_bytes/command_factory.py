from function_to_bytes.modbus_encoder import (
    create_modbus_write_command,
    create_modbus_read_command,
)

def initialize(slave_addr: int = 0x01) -> bytes:
    """
    그리퍼 초기화 명령 (0x0100에 0xA5 쓰기)
    """
    return create_modbus_write_command(slave_addr, 0x0100, 0xA5)

def set_force(slave_addr: int = 0x01, percent: int = 50) -> bytes:
    """
    Force 설정 (20~100%)
    """
    if not 20 <= percent <= 100:
        raise ValueError("Force must be between 20 and 100")
    return create_modbus_write_command(slave_addr, 0x0101, percent)

def set_position(slave_addr: int = 0x01, permil: int = 500) -> bytes:
    """
    위치 설정 (0~1000, 퍼밀 단위)
    """
    if not 0 <= permil <= 1000:
        raise ValueError("Position must be between 0 and 1000 (permil)")
    return create_modbus_write_command(slave_addr, 0x0103, permil)

def read_status(slave_addr: int = 0x01) -> bytes:
    """
    파지 상태 읽기 (0x0201)
    """
    return create_modbus_read_command(slave_addr, 0x0201, 1)

def read_position(slave_addr: int = 0x01) -> bytes:
    """
    현재 위치 읽기 (0x0202)
    """
    return create_modbus_read_command(slave_addr, 0x0202, 1)

def read_init_state(slave_addr: int = 0x01) -> bytes:
    """
    초기화 완료 여부 읽기 (0x0200)
    """
    return create_modbus_read_command(slave_addr, 0x0200, 1)

def disable_io_mode(slave_addr: int = 0x01) -> bytes:
    """
    I/O 모드 비활성화 (0x0402 = 0)
    """
    return create_modbus_write_command(slave_addr, 0x0402, 0)

def enable_io_mode(slave_addr: int = 0x01) -> bytes:
    """
    I/O 모드 활성화 (0x0402 = 1)
    """
    return create_modbus_write_command(slave_addr, 0x0402, 1)

def set_init_direction(slave_addr: int = 0x01, direction: int = 1) -> bytes:
    """
    초기화 방향 설정 (0 = 열림 방향, 1 = 닫힘 방향)
    """
    if direction not in (0, 1):
        raise ValueError("Direction must be 0 (open) or 1 (close)")
    return create_modbus_write_command(slave_addr, 0x0301, direction)
