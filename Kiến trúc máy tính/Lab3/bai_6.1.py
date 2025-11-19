import RPi.GPIO as gpio
import time

lcd_pins = {'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2}
lcd_width = 16
lcd_chr = True
lcd_cmd = False
lcd_line_1 = 0x80
lcd_line_2 = 0xC0
e_pulse = 0.0005
e_delay = 0.0005
dht11_pin = 7

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

def read_dht11():
    gpio.setup(dht11_pin, gpio.OUT)
    gpio.output(dht11_pin, gpio.LOW)
    time.sleep(0.02)
    gpio.output(dht11_pin, gpio.HIGH)
    gpio.setup(dht11_pin, gpio.IN)
    while gpio.input(dht11_pin) == gpio.LOW:
        pass
    while gpio.input(dht11_pin) == gpio.HIGH:
        pass
    data = []
    for i in range(40):
        while gpio.input(dht11_pin) == gpio.LOW:
            pass
        count = 0
        while gpio.input(dht11_pin) == gpio.HIGH:
            count += 1
            if count > 100:
                break
        if count > 8:
            data.append(1)
        else:
            data.append(0)
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]
    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    checksum = 0
    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7 - i)
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        checksum += check_bit[i] * 2 ** (7 - i)
    check = humidity + humidity_point + temperature + temperature_point
    if checksum == check:
        return temperature + temperature_point, humidity + humidity_point
    else:
        return None, None

def lcd_init():
    for pin in lcd_pins.values():
        gpio.setup(pin, gpio.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, lcd_cmd)

def lcd_clear():
    lcd_byte(0x01, lcd_cmd)

def lcd_byte(bits, mode):
    gpio.output(lcd_pins['RS'], mode)
    for bit_num in range(4):
        gpio.output(lcd_pins[f'D{bit_num + 4}'], bits & (1 << (4 + bit_num)) != 0)
    time.sleep(e_delay)
    gpio.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    gpio.output(lcd_pins['E'], False)
    time.sleep(e_delay)
    for bit_num in range(4):
        gpio.output(lcd_pins[f"D{bit_num + 4}"], bits & (1 << bit_num) != 0)
    time.sleep(e_delay)
    gpio.output(lcd_pins['E'], True)
    time.sleep(e_pulse)
    gpio.output(lcd_pins['E'], False)
    time.sleep(e_delay)

def lcd_display_string(message, line):
    lcd_byte(lcd_line_1 if line == 1 else lcd_line_2, lcd_cmd)
    for char in message:
        lcd_byte(ord(char), lcd_chr)

def main():
    lcd_init()
    gpio.output(lcd_pins['BL'], True)
    time.sleep(1)
    while True:
        temperature, humidity = read_dht11()
        print(temperature, humidity)
        if humidity is not None and temperature is not None:
            lcd_display_string('temp: {:.1f}C'.format(temperature), 1)
            lcd_display_string('humid: {:.1f}%'.format(humidity), 2)
            time.sleep(1)
        else:
            time.sleep(1)
try:
    main()
except KeyboardInterrupt:
    gpio.cleanup()
    lcd_clear()
