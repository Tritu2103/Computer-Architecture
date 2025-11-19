import RPi.GPIO as GPIO
import time

# Chân LCD
LCD_PINS = {'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2}
# Chân nút nhấn
BT_1 = 21

# Cấu hình LCD
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
E_PULSE = 0.0005
E_DELAY = 0.0005

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def lcd_init():
    for pin in LCD_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, LCD_CMD)


def lcd_clear():
    lcd_byte(0x01, LCD_CMD)


def lcd_byte(bits, mode):
    GPIO.output(LCD_PINS['RS'], mode)
    # 4 bit cao
    GPIO.output(LCD_PINS['D4'], bool(bits & 0x10))
    GPIO.output(LCD_PINS['D5'], bool(bits & 0x20))
    GPIO.output(LCD_PINS['D6'], bool(bits & 0x40))
    GPIO.output(LCD_PINS['D7'], bool(bits & 0x80))
    lcd_toggle_enable()
    # 4 bit thấp
    GPIO.output(LCD_PINS['D4'], bool(bits & 0x01))
    GPIO.output(LCD_PINS['D5'], bool(bits & 0x02))
    GPIO.output(LCD_PINS['D6'], bool(bits & 0x04))
    GPIO.output(LCD_PINS['D7'], bool(bits & 0x08))
    lcd_toggle_enable()


def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_PINS['E'], True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_PINS['E'], False)
    time.sleep(E_DELAY)


def lcd_display_string(message, line=LCD_LINE_1):
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)


def main():
    lcd_init()
    GPIO.output(LCD_PINS['BL'], True)
    button_state = 0
    msg = "Hello World"

    while True:
        if GPIO.input(BT_1) == GPIO.LOW:   # Nhấn nút
            button_state += 1
            time.sleep(0.3)  # chống dội nút

        # Lần 1: chạy từ trái sang phải
        if button_state == 1:
            for i in range(LCD_WIDTH - len(msg) + 1):
                lcd_clear()
                lcd_display_string(" " * i + msg, LCD_LINE_1)
                time.sleep(0.3)
                if GPIO.input(BT_1) == GPIO.LOW:  # nếu bấm tiếp thì thoát vòng lặp
                    button_state += 1
                    time.sleep(0.3)
                    break

        # Lần 2: chạy từ phải sang trái
        elif button_state == 2:
            for i in range(LCD_WIDTH - len(msg), -1, -1):
                lcd_clear()
                lcd_display_string(" " * i + msg, LCD_LINE_1)
                time.sleep(0.3)
                if GPIO.input(BT_1) == GPIO.LOW:
                    button_state += 1
                    time.sleep(0.3)
                    break

        # Lần 3: xoá và thoát
        elif button_state >= 3:
            lcd_clear()
            print("Thoát chương trình...")
            break


try:
    main()
except KeyboardInterrupt:
    lcd_clear()
    GPIO.cleanup()
