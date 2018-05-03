# Libraries
from StateMachine import StateMachine
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 4


class ElectroMagnet(threading.Thread):
    _states = ['initialized', 'on', 'off']

    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        threading.Thread.__init__(self)
        self.sm = StateMachine.get_magnet_machine(self, ElectroMagnet._states)

    def run(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("[ Electromagnet ] ON")
        while self.is_on():
            pass

    def clean_up(self):

        GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    def get_sm(self):
        return self.sm