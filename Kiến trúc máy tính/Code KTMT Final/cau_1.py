import RPi.GPIO as GPIO
import time
LCD_PINS = {'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2}
BTS = {"BT_1": 21, "BT_2": 26, "BT_3": 20, "BT_4": 19}
LED = 13
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
E_PULSE = 0.0005
E_DELAY = 0.0005
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)
def pull_up_bts():
    for pin in BTS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def lcd_init():
    for pin in LCD_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, LCD_CMD)
def lcd_clear():
    lcd_byte(0x01, LCD_CMD)
def lcd_byte(bits, mode):
    GPIO.output(LCD_PINS['RS'], mode)
    for bit_num in range(4):
        GPIO.output(LCD_PINS[f'D{bit_num + 4}'], bits & (1 << (4 + bit_num)) != 0)
    time.sleep(E_DELAY)
    GPIO.output(LCD_PINS['E'], True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_PINS['E'], False)
    time.sleep(E_DELAY)
    for bit_num in range(4):
        GPIO.output(LCD_PINS[f'D{bit_num + 4}'], bits & (1 << bit_num) != 0)
    time.sleep(E_DELAY)
    GPIO.output(LCD_PINS['E'], True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_PINS['E'], False)
    time.sleep(E_DELAY)
def lcd_display_string(message, line):
    lcd_byte(LCD_LINE_1 if line == 1 else LCD_LINE_2, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

# Viết chương trình theo kịch bản sau, nhấn lần lượt theo thứ tự nút bấm 1, nút bấm 2 thì LED sáng,
# nhấn lần lượt theo thứ tự nút bấm 3, nút bấm 4 thì đèn nền LCD sáng,
# nhấn giữ đồng thời nút bấm 1 và nút bấm 3 thì cả hai LED và đèn nền LCD tắt
def main():
    lcd_init()
    while True:
        if GPIO.input(BTS["BT_1"]) == GPIO.LOW:
            time.sleep(0.25)
            while True:
                if GPIO.input(BTS["BT_2"]) == GPIO.LOW:
                    GPIO.output(LED, GPIO.HIGH)
                    time.sleep(0.25)
                    break

        if GPIO.input(BTS["BT_3"]) == GPIO.LOW:
            time.sleep(0.25)
            while True:
                if GPIO.input(BTS["BT_4"]) == GPIO.LOW:
                    GPIO.output(LCD_PINS['BL'], True)
                    time.sleep(0.25)
                    break

        if GPIO.input(BTS["BT_1"]) == GPIO.LOW and GPIO.input(BTS["BT_3"]) == GPIO.LOW:
            GPIO.output(LED, GPIO.LOW)
            GPIO.output(LCD_PINS['BL'], False)

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd_clear()