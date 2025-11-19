from PIL import Image, ImageDraw, ImageFont
import spidev
import time
import numpy as np

# --- SPI init ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000000
spi.mode = 0b00

def max7219_write(register, data):
    spi.xfer2([register, data])

def max7219_init():
    max7219_write(0x0F, 0x00)  # test off
    max7219_write(0x09, 0x00)  # no decode
    max7219_write(0x0A, 0x08)  # intensity (0x00..0x0F)
    max7219_write(0x0B, 0x07)  # scan limit = all 8 rows
    max7219_write(0x0C, 0x01)  # normal operation (not shutdown)

def clear_matrix():
    for row in range(1, 9):
        max7219_write(row, 0x00)

def create_text_image(text):
    width = 8 * len(text)
    height = 8
    image = Image.new('1', (width, height), 0)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, -1), text, font=font, fill=1)
    return image

def display_image(image8x8):
    # image8x8 must be exactly 8x8
    pixels = np.array(image8x8)
    for y in range(8):
        row_data = 0
        for x in range(8):
            if pixels[y, x]:
                # NOTE: nếu hàng bị đảo trái/phải, đổi (7-x) <-> x
                row_data |= 1 << (7 - x)
        max7219_write(y + 1, row_data)

def main():
    max7219_init()
    digits = "0 1 2 3 4 5 6 7 8 9 "   # có space giữa cho khoảng cách
    text = digits * 3  # lặp để cuộn liên tục mượt hơn
    image = create_text_image(text)

    # xoay toàn bộ ảnh 180 độ (yêu cầu của bạn)
    rotated = image.rotate(180)

    try:
        while True:
            # +1 để bao gồm vị trí cuối cùng
            for x in range(0, rotated.width - 8 + 1):
                cropped = rotated.crop((x, 0, x + 8, 8))
                display_image(cropped)
                time.sleep(0.12)  # tốc độ cuộn (thay đổi theo ý bạn)
    except KeyboardInterrupt:
        clear_matrix()
        spi.close()
        print("Stopped.")

