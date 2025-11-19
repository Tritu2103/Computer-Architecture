import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 13
GPIO.setup(LED, GPIO.OUT)


def toggleLED(state, duration):
    GPIO.output(LED, state)
    time.sleep(duration)


try:
    while True:
        toggleLED(GPIO.HIGH, 1)
        toggleLED(GPIO.LOW, 2)
        toggleLED(GPIO.HIGH, 3)
        toggleLED(GPIO.LOW, 1)
except KeyboardInterrupt:
    GPIO.cleanup()