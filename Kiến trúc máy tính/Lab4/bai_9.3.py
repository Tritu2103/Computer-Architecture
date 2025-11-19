import RPi.GPIO as GPIO
import time

lcd_pins = {
    'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2
}
lcd_width = 16
lcd_chr = True
lcd_cmd = False
lcd_line_1 = 0x80
lcd_line_2 = 0xC0
e_pulse = 0.0005
e_delay = 0.0005
light_ss = 5
pwm_pin = 24
dir_pin = 25
servo_pin = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwm_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(light_ss, GPIO.IN)
pwm_dc = GPIO.PWM(pwm_pin, 1000)
pwm_dc.start(0)
servo_pwm = GPIO.PWM(servo_pin, 50)
servo_pwm.start(0)
curtain_is_open = None

def lcd_init():
    for pin in lcd_pins.values():
        GPIO.setup(pin, GPIO.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, lcd_cmd)

def lcd_clear():
    lcd_byte(0x01, lcd_cmd)

def lcd_byte(bits, mode):
    GPIO.output(lcd_pins['RS'], mode)
    for bit_num in range(4):
        GPIO.output(lcd_pins[f'D{bit_num+4}'], bits & (1 << (4+bit_num)) != 0)
    time.sleep(e_delay)
    GPIO.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    GPIO.output(lcd_pins['E'], False)
    time.sleep(e_delay)
    for bit_num in range(4):
        GPIO.output(lcd_pins[f'D{bit_num+4}'], bits & (1 << bit_num) != 0)
    time.sleep(e_delay)
    GPIO.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    GPIO.output(lcd_pins['E'], False)
    time.sleep(e_delay)

def lcd_display_string(message, line):
    lcd_byte(lcd_line_1 if line == 1 else lcd_line_2, lcd_cmd)
    for char in message:
        lcd_byte(ord(char), lcd_chr)

def set_servo_angle(angle):
    duty = angle / 18
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo_pwm.ChangeDutyCycle(0)

def motor_control(speed, direction):
    GPIO.output(dir_pin, direction)
    if direction == 0:
        speed = speed
    else:
        speed = 100 - speed
    pwm_dc.ChangeDutyCycle(speed)

def main():
    global curtain_is_open
    lcd_init()
    while True:
        light_status = GPIO.input(light_ss)
        if light_status and curtain_is_open != False:
            lcd_display_string("toi: dong rem", 1)
            set_servo_angle(30)
            motor_control(60,1)
            time.sleep(3)
            motor_control(0,0)
            curtain_is_open = False
        elif not light_status and curtain_is_open != True:
            
            lcd_display_string("sang: mo rem", 1)
            set_servo_angle(120)
            motor_control(60, 0)
            time.sleep(3)
            motor_control(0,0)
            curtain_is_open = True
        time.sleep(1)

try: main()
except KeyboardInterrupt: GPIO.cleanup(); lcd_clear(); pwm_dc.stop(); servo_pwm.stop()