import RPi.GPIO as GPIO
import time

LED_RED = 11
LED_GREEN = 13
LED_YELLOW = 15
BUZZER = 37

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)

def turn_led_on(led):
    GPIO.output(led, GPIO.HIGH)

def turn_led_off(led):
    GPIO.output(led, GPIO.LOW)

def turn_green_on():
    turn_led_off(LED_RED)
    turn_led_off(LED_YELLOW)
    turn_led_on(LED_GREEN)

def turn_red_on():
    turn_led_off(LED_GREEN)
    turn_led_off(LED_YELLOW)
    turn_led_on(LED_RED)

def play_sound(sound_time=0.1):
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(sound_time)
    GPIO.output(BUZZER, GPIO.LOW)
