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


class StepperH(threading.Thread):
    _states = ['initialised', 'running_forwards', 'running_backwards', 'stopped']

    def __init__(self):
        threading.Thread.__init__(self)
        self.delay = 0.05
        self.count = 5
        self.sm = StateMachine.get_stepperh_machine(self, StepperH._states)

    def run(self):
        print("\nStepperH ON")

        while self.is_running_forwards():
            self.do_steps()

        self.clean_up()

        print("[StepperH]: Waiting for state change")
        while self.is_stopped():
            pass

        while self.is_running_forwards():
            self.do_steps()

    def do_steps(self):
        if self.delay > 0.0005:
            self.delay = math.exp(-self.count) + 0.0005
            self.count = self.count + 0.02

        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)

    @staticmethod
    def clean_up():
        print("\nStepperH OFF")
        GPIO.cleanup()
