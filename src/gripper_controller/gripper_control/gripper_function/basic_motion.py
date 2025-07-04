from gripper_control.gripper_function.motion import set_force_level, move_to_position
def close(client, slave_addr=0x01, force=70, permil=850):
    """
    물체 유무와 무관하게 강하게 닫기 (센서 피드백 없이 동작만)
    """
    print(f"🔒 Gripper Close → Force: {force}%, Position: {permil}")
    set_force_level(client, percent=force, slave_addr=slave_addr)
    move_to_position(client, permil=permil, slave_addr=slave_addr)

def open(client, slave_addr=0x01, force=30, permil=100):
    """
    그리퍼 열기 (센서 피드백 없이 동작만)
    """
    print(f"🔓 Gripper Open → Force: {force}%, Position: {permil}")
    set_force_level(client, percent=force, slave_addr=slave_addr)
    move_to_position(client, permil=permil, slave_addr=slave_addr)