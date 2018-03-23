# Libraries
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 4
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)


class ElectroMagnet(threading.Thread):

    def __init__(self):
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("Electromagnet ON")
        while self.running:
            print("Electromagnet still running...")
            time.sleep(5)

    def clean_up(self):
        print("\nElectromagnet OFF")
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
	self.running = False
