import cv2
import RPi.GPIO as GPIO
import numpy as np

def main():
    BT1 = 21
    BT2 = 20  # Thêm nút BT2
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(0)
    print("Capture ready")

    while True:
        ret, frame = capture.read()
        if GPIO.input(BT1) == GPIO.LOW:
            print("Nhan Button 1")
            cv2.imshow("Anh chup camera", frame)
            cv2.waitKey(0)  # Hiển thị ảnh chụp
            cv2.destroyWindow("Anh chup camera")

        if GPIO.input(BT2) == GPIO.LOW:
            print("Nhan Button 2")
            # Xử lý ảnh để đếm pixel màu đỏ
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(hsv,(0,118,130),(5,255,255))
            red_pixel_count = cv2.countNonZero(red_mask)
            print(f"Red Pixels: {red_pixel_count}")

try:
    main()
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    GPIO.cleanup()
