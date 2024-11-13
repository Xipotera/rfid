import os
import socketio
from threading import Thread

# Initialisation du client Socket.IO
sio = socketio.Client()
socketio_url = os.getenv("SOCKETIO_URL", "http://localhost:4020")


# Événement de connexion
@sio.event
def connect():
    print("Connected to Socket.IO server")
    # Rejoindre une room dès la connexion, par exemple 'room1'
    join_room("room1")


# Événement de déconnexion
@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")


# Écouter les messages provenant du serveur
@sio.on("response")
def on_message(data):
    print(f"Message from server: {data}")


# Fonction pour rejoindre une room
def join_room(room_name):
    if sio.connected:
        sio.emit("joinRoom", room_name)
        print(f"Joined room: {room_name}")


# Fonction pour envoyer un tag individuellement
def send_to_socketio(tag, RFID_Time):
    if sio.connected:
        data = {
            "tag": tag,
            "date": RFID_Time.strftime("%Y-%m-%d"),
            "time": RFID_Time.strftime("%H:%M:%S.%f"),
        }
        sio.emit("message", data)
        print(f"Data sent to Socket.IO: {data}")


# Démarrer le client Socket.IO dans un thread
def start_socketio():
    def run():
        sio.connect(socketio_url)
        sio.wait()

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
