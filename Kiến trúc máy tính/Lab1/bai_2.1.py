import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ledPin = 13
GPIO.setup(ledPin, GPIO.OUT)
count = 0
try:
    while True:
        GPIO.output(ledPin, GPIO.HIGH)
        count += 1
        print("den sang {} lan." .format(count))
        time.sleep(1)
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
