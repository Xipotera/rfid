import os
import socketio
from threading import Thread

# Initialisation du client Socket.IO
sio = socketio.Client()
socketio_url = os.getenv("SOCKETIO_URL", "http://localhost:4020")

@sio.event
def connect():
    print("Connected to Socket.IO server")

@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")

@sio.on("response")
def on_message(data):
    print(f"Message from server: {data}")

def send_to_socketio(tag, RFID_Time):
    if sio.connected:
        data = {
            "tag": tag,
            "date": RFID_Time.strftime('%Y-%m-%d'),
            "time": RFID_Time.strftime('%H:%M:%S.%f')
        }
        sio.emit("message", data)
        print(f"Data sent to Socket.IO: {data}")

def start_socketio():
    def run():
        sio.connect(socketio_url)
        sio.wait()

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
