# Libraries
from StateMachine import StateMachine
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 4
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)


def add_transitions(machine):
    machine.add_transitions(target='power_on',
                            source='initialised',
                            dest='on')
    machine.add_transitions(target='power_on',
                            source='off',
                            dest='on')

    machine.add_transitions(target='power_off',
                            source='on',
                            dest='off')


class ElectroMagnet(threading.Thread):
    _states = ['initialised', 'on', 'off']

    def __init__(self):
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        threading.Thread.__init__(self)
        self.sm = StateMachine.get_stepperh_machine(self, ElectroMagnet._states)
        add_transitions(self.sm)

    def run(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("Electromagnet ON")
        while self.is_on():
            print("Electromagnet still running...")
            time.sleep(5)

    def clean_up(self):
        print("\nElectromagnet OFF")
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
