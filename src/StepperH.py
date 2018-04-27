from time import sleep
from StateMachine import StateMachine
import math
import RPi.GPIO as GPIO
import threading
from Observable import Observable

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


class StepperH(threading.Thread, Observable):
    _states = ['initialised', 'running_forwards', 'running_backwards', 'stopped']
    position = [0, 0]

    def __init__(self):
        print("[ StepperH ] initialising")
        threading.Thread.__init__(self)
        Observable.__init__(self)
        self.amount_of_steps = 0
        self.steps_taken = 0
        self.delay = 0.05
        self.count = 5
        self.sm = StateMachine.get_stepperh_machine(self, StepperH._states)
        print("[ StepperH ] Set delay between steps to " + str(self.delay) + "s")
        print("[ StepperH ] initialized")

    def run(self):
        print("[ StepperH ] ON")
        print("[ StepperH ] Steps taken: "+str(self.steps_taken))
        print("[ StepperH ] Steps to take: " + str(self.amount_of_steps))

        while self.steps_taken < self.amount_of_steps:
            self.do_steps()

        print("[ StepperH ] OFF")
        print("[ StepperH ] Stepper took "+str(self.steps_taken)+" before stopping")
        print("[ StepperH ] Waiting for state change")

        self.stop_stepperH()

        while self.is_stopped():
            pass

        while self.steps_taken < self.amount_of_steps:
            self.do_steps()
            print("hello")
            print("[ StepperH ] Steps taken: "+str(self.steps_taken)+", Steps to take: "+str(self.amount_of_steps))
        self.clean_up()

    def get_sm(self):
        return self.sm

    def do_steps(self):
        if self.delay > 0.0005:
            self.delay = math.exp(-self.count) + 0.0005
            self.count = self.count + 0.02

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)
        self.steps_taken += 1
        self.update_position()
        Observable.dispatch(self, str(self.get_x()) + ";" + str(self.get_y()))

    def update_position(self):
        self.position[0] += 1
        self.position[1] += 1

    def get_x(self):
        return self.position[0]

    def get_y(self):
        # To set to actual y-steps
        return 200

    def set_distance(self, steps):
        self.amount_of_steps = int(steps)
        print("[ StepperH ] Set amount of steps to " + str(self.amount_of_steps))

    @staticmethod
    def set_direction(direction):
        GPIO.output(DIR, direction)
        print("[ StepperH ]"
              " Set direction to "+str(direction))

    @staticmethod
    def clean_up():
        GPIO.cleanup()
