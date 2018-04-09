from time import sleep
from StateMachine import StateMachine
import math
import RPi.GPIO as GPIO
import threading

DIR = 24  # Direction GPIO Pin
STEP = 23  # Step GPIO Pin
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 1000  # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# set direction forward (clockwise)
GPIO.output(DIR, CCW)

step_count = SPR
delay = .0005


def add_transitions(machine):
    machine.add_transition(trigger='start',
                           source='initialised',
                           dest='running_forwards')

    machine.add_transition(trigger='change_to_forwards',
                           source='running_forwards',
                           dest='running_backwards')
    machine.add_transition(trigger='change_to_backwards',
                           source='running_backwards',
                           dest='running_forwards')

    machine.add_transition(trigger='stop',
                           source='running_forwards',
                           dest='stopped')
    machine.add_transition(trigger='stop',
                           source='running_backwards',
                           dest='stopped')

    machine.add_transition(trigger='resume_forwards',
                           source='stopped',
                           dest='running_forwards')
    machine.add_transition(trigger='resume_backwards',
                           source='stopped',
                           dest='running_backwards')


class StepperH(threading.Thread):
    _states = ['initialised', 'running_forwards', 'running_backwards', 'stopped']

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.breaking = True
        self.delay = 0.05
        self.count = 5
        self.sm = StateMachine.get_stepperh_machine(self, StepperH._states)
        add_transitions(self.sm)

    def run(self):
        print("\nStepperH ON")

        while self.running:
            if self.delay > 0.0005:
                self.delay = math.exp(-self.count) + 0.0005
                self.count = self.count + 0.02

        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)

        while self.breaking:
            if self.delay < 0.005:
                self.delay = math.exp(-self.count) + 0.0005
                self.count = self.count - 0.1
            else:
                self.breaking = False
            GPIO.output(STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(self.delay)
            GPIO.cleanup()

    def clean_up(self):
        print("\nStepperH OFF")
        self.running = False
