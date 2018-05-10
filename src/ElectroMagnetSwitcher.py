from ElectroMagnet import ElectroMagnet

# Libraries
from StateMachine import StateMachine
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 4

def add_magnet_transitions(machine):
    machine.add_transition(trigger='power_on',
                            source='initialized',
                            dest='on')
    machine.add_transition(trigger='power_on',
                            source='off',
                            dest='on')

    machine.add_transition(trigger='power_off',
                            source='on',
                            dest='off')


class ElectroMagnet(threading.Thread):
    _states = ['initialized', 'on', 'off']

    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        self.running = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        threading.Thread.__init__(self)
        self.sm = StateMachine.get_magnet_machine(self, ElectroMagnet._states)

    def run(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("[ Electromagnet ] ON")
        while self.running:
            pass

    def clean_up(self):
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    def get_sm(self):
        return self.sm


if __name__ == '__main__':
    magnet = ElectroMagnet()
    add_magnet_transitions(magnet.get_sm())
    running = True

    try:
        magnet.start()
        while True:
            pass
    except KeyboardInterrupt:
        magnet.running = False
        magnet.clean_up()