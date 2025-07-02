import serial

def hex_str_to_bytes(hex_str):
    # 공백 제거 + 16진수 문자열을 바이트로 변환
    hex_str = hex_str.strip().replace(" ", "")
    return bytes.fromhex(hex_str)

def main():
    # 시리얼 포트 설정 (윈도우: COMx, 리눅스: /dev/ttyUSB0)
    ser = serial.Serial(port='COM6', baudrate=115200, timeout=1)

    print("==== RS-485 그리퍼 통신 ====")
    print("16진수 명령어를 입력하세요 (예: 01 06 01 00 01 49 F6)\n종료하려면 'exit' 입력")

    while True:
        cmd = input("Send (hex): ")
        if cmd.lower() == 'exit':
            break

        try:
            tx_bytes = hex_str_to_bytes(cmd)
            ser.write(tx_bytes)
            response = ser.read(32)  # 최대 32바이트 읽기
            print("Recv (hex):", response.hex(" ").upper())
        except Exception as e:
            print("❌ 오류:", e)

    ser.close()
    print("연결 종료.")

if __name__ == "__main__":
    main()
