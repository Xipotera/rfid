import signal
import time
from config.settings import load_environment
from services.socket_client import start_socketio, send_to_socketio
from services.gpio_control import turn_green_on, turn_red_on, play_sound, setup_gpio
from services.rfid_reader import set_up_the_reader, send_command, read_buffer
from utils.helpers import exit_gracefully

# Charger les variables d'environnement
load_environment()

# Initialisation de GPIO et des signaux de sortie
setup_gpio()
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

# Variables globales
detected_tags = set()

# Lancer le client Socket.IO
start_socketio()

# Configuration du lecteur RFID
set_up_the_reader()

# Boucle principale
try:
    while True:
        send_command()
        tags, RFID_Time = read_buffer()
        for tag in tags:
            tag = f"U{tag.strip()}"
            if len(tag) != 33 or not tag[1:].isalnum():
                continue

            if tag not in detected_tags:
                print("Nouveau tag détecté :", tag)
                detected_tags.add(tag)
                send_to_socketio(tag, RFID_Time)
                turn_green_on()
                play_sound()
            else:
                turn_red_on()
                play_sound(0.5)

            time.sleep(1)

except Exception as e:
    print(f"Erreur rencontrée : {e}")
    exit_gracefully(None, None)
