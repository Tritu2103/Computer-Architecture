import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

pwm_pin = 24
dir_pin = 25

gpio.setup(pwm_pin, gpio.OUT)
gpio.setup(dir_pin, gpio.OUT)
pwm = gpio.PWM(pwm_pin, 1000)
pwm.start(0)

def motor_control(speed, direction):
    gpio.output(dir_pin, direction)
    pwm.ChangeDutyCycle(speed)

def main():
    while True:
        motor_control(50, 0)

try:
    main()
except KeyboardInterrupt:
    pwm.stop()
    gpio.cleanup()