# Libraries
from StateMachine import StateMachine
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 4


class ElectroMagnet:
    _states = ['initialized', 'on', 'off']

    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        self.running = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        self.sm = StateMachine.get_magnet_machine(self, ElectroMagnet._states)

    def on(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("[ Electromagnet ] ON")

    def off(self):
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        print("[ Electromagnet ] OFF")

    def get_sm(self):
        return self.sm