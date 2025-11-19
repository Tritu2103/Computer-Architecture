import time
from pickle import FALSE

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 13
BT_1 = 21
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ledState = FALSE


def updateLED():
    global ledState
    if GPIO.input(BT_1) == GPIO.LOW:
        ledState = not ledState
        GPIO.output(LED, ledState)
        time.sleep(0.25)


try:
    while True:
        updateLED()
except KeyboardInterrupt:
    GPIO.cleanup()