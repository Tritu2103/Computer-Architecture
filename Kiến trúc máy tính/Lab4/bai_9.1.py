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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

def main():
    lcd_init()
    GPIO.setup(light_ss, GPIO.IN, GPIO.PUD_UP)
    GPIO.output(lcd_pins['BL'], True)
    while True:
        if GPIO.input(light_ss) == 0:
            lcd_display_string("sang", 1)
        else:
            lcd_display_string("toi", 1)
        time.sleep(0.5)

try: main()
except KeyboardInterrupt: GPIO.cleanup(); lcd_clear()