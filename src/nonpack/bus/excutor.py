import time
class CommandExecutor:
    def __init__(self, client, slave_id=0x01):
        self.client = client
        self.slave_id = slave_id

    def execute(self, label, cmd_bytes, wait_for=None, timeout=5.0):
        """
        label: 명령 이름 (예: "Force 설정")
        cmd_bytes: 전송할 바이트
        wait_for: 'init' / 'motion' / None
        """
        print(f"📤 Sending {label} command: {cmd_bytes.hex().upper()}")
        self.client.socket.write(cmd_bytes)
        time.sleep(0.1)
        resp = self.client.socket.read(8)
        print(f"📥 {label} Response: {resp.hex().upper()}")

        # 예외 응답 해석
        from bus.reader import parse_modbus_exception_response
        result = parse_modbus_exception_response(resp)
        if isinstance(result, dict):
            raise RuntimeError(f"❌ {label} 실패 → {result['meaning']}")

        print(f"✅ {label} 명령 수신 성공")

        # 후속 상태 확인
        if wait_for == "init":
            self.wait_until_initialized(timeout)
        elif wait_for == "motion":
            self.wait_until_motion_complete(timeout)

    def wait_until_initialized(self, timeout=5.0):
        from bus.function_to_bytes import read_init_state
        cmd = read_init_state(self.slave_id)
        start = time.time()
        while time.time() - start < timeout:
            self.client.socket.write(cmd)
            time.sleep(0.1)
            resp = self.client.socket.read(7)
            if resp[1] == 0x03 and resp[3] == 0x00 and resp[4] == 0x01:
                print("✅ Initialization 완료됨")
                return
        raise TimeoutError("❌ Initialization 완료 대기 실패")

    def wait_until_motion_complete(self, timeout=5.0):
        from bus.function_to_bytes import read_status, parse_status_response
        cmd = read_status(self.slave_id)
        start = time.time()
        while time.time() - start < timeout:
            self.client.socket.write(cmd)
            time.sleep(0.1)
            resp = self.client.socket.read(7)
            parsed = parse_status_response(resp)
            print(f"🔄 Status: {parsed}")
            if "도달" in parsed or "파지" in parsed:
                print("✅ 동작 완료됨")
                return
        raise TimeoutError("❌ 동작 완료 대기 실패")
