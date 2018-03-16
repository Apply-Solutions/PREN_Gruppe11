import RPi as GPIO
import time


def distance():
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO_ECHO = 16
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    return GPIO.input(GPIO_ECHO)


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print(dist)
            time.sleep(1)
    except KeyboardInterrupt:
        print("stopped")
