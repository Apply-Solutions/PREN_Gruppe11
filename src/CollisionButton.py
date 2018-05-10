from Observable import Observable
import RPi.GPIO as GPIO
import time

GPIO_ECHO = 19


class CollisionButton(Observable):

    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        # set GPIO Pins

        # set GPIO input (IN / OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self.has_collided = False

    def detect_collision(self):
        while not self.has_collided:
            self.has_collided = GPIO.input(GPIO_ECHO)
            time.sleep(.5)

    @staticmethod
    def has_collided():
        return GPIO.input(GPIO_ECHO)