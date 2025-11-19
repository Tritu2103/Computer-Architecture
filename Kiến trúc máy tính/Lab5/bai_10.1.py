import RPi.GPIO as GPIO
import time
lcd_pins = {'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2}
lcd_width = 16
lcd_chr = True
lcd_cmd = False
lcd_line_1 = 0x80
lcd_line_2 = 0xC0
e_pulse = 0.0005
e_delay = 0.0005
bt_1 = 21
trig = 15
echo = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(bt_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)
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
        GPIO.output(lcd_pins[f'D{bit_num + 4}'], bits & (1 << (4 + bit_num)) != 0)
    time.sleep(e_delay)
    GPIO.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    GPIO.output(lcd_pins['E'], False)
    time.sleep(e_delay)
    for bit_num in range(4):
        GPIO.output(lcd_pins[f'D{bit_num + 4}'], bits & (1 << bit_num) != 0)
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
    lcd_init()
    GPIO.output(lcd_pins['BL'],True)
    global pulse_end
    while True:
        if GPIO.input(bt_1) == 0:
            lcd_display_string("dang thuc hien do",1)
            time.sleep(2)
            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig, False)
            while GPIO.input(echo) == 0:
                pulse_start = time.time()
            while GPIO.input(echo) == 1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            if distance > 100:
                lcd_display_string("ERROR",1)
            else:
                lcd_display_string(f"Distance:{distance}cm",1)
            time.sleep(1)
try:
    main()
except KeyboardInterrupt:
    lcd_clear()
    GPIO.cleanup()
