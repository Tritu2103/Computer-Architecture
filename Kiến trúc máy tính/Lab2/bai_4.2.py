import time

import RPi.GPIO as GPIO

RELAY_1 = 16
RELAY_2 = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY_1, GPIO.OUT)
GPIO.setup(RELAY_2, GPIO.LOW)
try:
    while True:
        GPIO.output(RELAY_1, GPIO.HIGH)
        GPIO.output(RELAY_2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(RELAY_1, GPIO.LOW)
        GPIO.output(RELAY_2, GPIO.HIGH)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
