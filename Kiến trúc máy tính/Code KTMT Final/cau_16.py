import cv2
import RPi.GPIO as GPIO
import numpy as np
import time
def main():
    BT1 = 21
    BT2 = 20
    RELAY1 = 16
    RELAY2 = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RELAY1, GPIO.OUT)
    GPIO.setup(RELAY2, GPIO.OUT)

    GPIO.output(RELAY1, GPIO.LOW)
    GPIO.output(RELAY2, GPIO.LOW)
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
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(hsv,(0,118,130),(5,255,255))
            green_mask = cv2.inRange(hsv, (35, 89, 107), (45, 241, 213))
            red_pixel_count = cv2.countNonZero(red_mask)
            green_pixel_count = cv2.countNonZero(green_mask)
            print(f"Red Pixels: {red_pixel_count}")
            print(f"Green Pixels: {green_pixel_count}")
            if red_pixel_count > green_pixel_count:
                print("Red lon hon, bat Role 1")
                GPIO.output(RELAY1, GPIO.HIGH)
                GPIO.output(RELAY2, GPIO.LOW)
            else:
                print("Xanh lon hon,bat Role 2")
                GPIO.output(RELAY1, GPIO.LOW)
                GPIO.output(RELAY2, GPIO.HIGH)

            time.sleep(0.2)

try:
    main()
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    GPIO.cleanup()
