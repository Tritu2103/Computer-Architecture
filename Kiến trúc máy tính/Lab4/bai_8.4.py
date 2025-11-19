import RPi.GPIO as GPIO
import time

# Servo pin
servo = 6

# LCD pins
lcd_pins = {
    'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2
}

# Button pins (chỉnh lại để không bị trùng)
buttons = {
    "bt_1": 26,   # giảm góc
    "bt_2": 20,   # tăng góc
    "bt_3": 16    # reset về 90°
}

# LCD settings
lcd_width = 16
lcd_chr = True
lcd_cmd = False
lcd_line_1 = 0x80
lcd_line_2 = 0xC0
e_pulse = 0.0005
e_delay = 0.0005

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servo, GPIO.OUT)

# Setup buttons
for button in buttons.values():
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM for servo
pwm = GPIO.PWM(servo, 50)
pwm.start(0)

# Servo state
current_angle = 90

def set_servo_angle(angle):
    duty = angle / 18
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

# LCD functions
def lcd_init():
    for pin in lcd_pins.values():
        GPIO.setup(pin, GPIO.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, lcd_cmd)

def lcd_clear():
    lcd_byte(0x01, lcd_cmd)

def lcd_byte(bits, mode):
    GPIO.output(lcd_pins['RS'], mode)

    # High nibble
    for bit_num in range(4):
        GPIO.output(lcd_pins[f'D{bit_num+4}'], bits & (1 << (4+bit_num)) != 0)
    time.sleep(e_delay)
    GPIO.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    GPIO.output(lcd_pins['E'], False)
    time.sleep(e_delay)

    # Low nibble
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

def main():
    global current_angle
    lcd_init()
    set_servo_angle(current_angle)
    while True:
        if GPIO.input(buttons["bt_1"]) == GPIO.LOW:
            print("press button 1")
            time.sleep(0.1)
            while GPIO.input(buttons["bt_1"]) == GPIO.LOW:
                print("hold button 1")
                current_angle = max(10, current_angle - 10)
                set_servo_angle(current_angle)
                lcd_display_string(f"Goc quay: {current_angle}°", 1)

        if GPIO.input(buttons["bt_2"]) == GPIO.LOW:
            print("press button 2")
            time.sleep(0.1)
            while GPIO.input(buttons["bt_2"]) == GPIO.LOW:
                print("hold button 2")
                current_angle = min(160, current_angle + 10)
                set_servo_angle(current_angle)
                lcd_display_string(f"Goc quay: {current_angle}°", 1)

        if GPIO.input(buttons["bt_3"]) == GPIO.LOW:
            print("press button 3")
            time.sleep(0.1)
            while GPIO.input(buttons["bt_3"]) == GPIO.LOW:
                print("hold button 3")
                current_angle = 90
                set_servo_angle(current_angle)
                lcd_display_string(f"Goc quay: {current_angle}°", 1)

try:
    main()
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    lcd_clear()
