from StateMachine import StateMachine
from time import sleep
import RPi.GPIO as GPIO
import threading

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1000   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# set direction downward (clockwise)
GPIO.output(DIR, CW)

step_count = SPR
delay = .0005  # in seconds (.005 = 5ms)


class StepperV(threading.Thread):
    _states = ['initialised', 'running_upwards', 'running_downwards', 'stopped']

    current_pos = 0
    has_cargo = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.sm = StateMachine.get_stepperh_machine(self, StepperV._states)

    def run(self):
        print("\nStepperV ON")
        while not self.is_stopped():
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

    def calculate_pos(self):
        pass

    def get_sm(self):
        return self.sm

    @staticmethod
    def change_direction(self):
        GPIO.output(DIR, CCW)

    @staticmethod
    def clean_up():
        print("\nStepperV OFF")
        GPIO.cleanup()