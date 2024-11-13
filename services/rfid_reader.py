import serial
import time
import datetime

# Configuration du port série
serial_port = "/dev/ttyUSB0"
ser = serial.Serial(
    port=serial_port,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)


def set_up_the_reader(power_level="25"):
    print("Configuration du lecteur RFID...")
    ser.write(f"\nN1,{power_level}\r".encode())
    ser.write(b"\nN5,05\r")
    print(
        "Lecteur configuré pour l'Europe avec une " "puissance de sortie de",
        power_level,
    )


def send_command():
    reader_command = "\nU\r"
    ser.write(reader_command.encode())
    time.sleep(0.1)


def read_buffer():
    RFID_Tags = ser.read(ser.inWaiting()).decode("utf-8", errors="ignore")
    RFID_Time = datetime.now()
    tags = RFID_Tags.strip().split("U")[1:]
    return tags, RFID_Time
