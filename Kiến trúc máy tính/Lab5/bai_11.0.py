import RPi.GPIO as GPIO
import time
CLK = 11
DIN = 10
CS = 8
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

def spi_send_byte(register, data):
    GPIO.output(CS, GPIO.LOW)
    for bit in range(8):
        GPIO.output(CLK, GPIO.LOW)
        GPIO.output(DIN, (register >> (7 - bit)) & 0x01)
        GPIO.output(CLK, GPIO.HIGH)

    for bit in range(8):
        GPIO.output(CLK, GPIO.LOW)
        GPIO.output(DIN, (data >> (7 - bit)) & 0x01)
        GPIO.output(CLK, GPIO.HIGH)
    GPIO.output(CS, GPIO.HIGH)

def max7219_init():
    spi_send_byte(0x0F, 0x00) #kiem tra hien thi
    spi_send_byte(0x09, 0x00) #che do giai ma(ko su dung chuc nang giai ma vi chgta kiem soat truc tiep tung LED)
    spi_send_byte(0x0B, 0x07) #gioi han quet(dam bao rang chgta co the hiem soat toan bo LED ma tran 8x8)
    spi_send_byte(0x0A, 0x00) #cuong do sang(toi da la 0x0F, thap nhat la 0x00)
    spi_send_byte(0x0C, 0x01) #tat thanh ghi

def clear_display():
    for row in range(1, 9):
        spi_send_byte(row, 0x00)

def main():
    max7219_init()
    clear_display()
    while True:
        spi_send_byte(0x0F, 0x01)

try:
    main()
except KeyboardInterrupt:
    clear_display()
    GPIO.cleanup()