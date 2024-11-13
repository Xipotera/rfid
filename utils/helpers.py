import sys
import RPi.GPIO as GPIO
from services.rfid_reader import ser


def exit_gracefully(signum, frame):
    print("\nFermeture du script... Nettoyage en cours.")
    ser.close()
    GPIO.cleanup()
    print("Port série et GPIO nettoyés.")
    sys.exit(0)
