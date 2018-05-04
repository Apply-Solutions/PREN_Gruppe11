from StateMachine import StateMachine
from time import sleep
import RPi.GPIO as GPIO
import threading

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1000   # Steps per Revolution (360 / 7.5)
delay = 0.0005  # in seconds (.005 = 5ms)


class StepperV(threading.Thread):
    _states = ['initialized', 'running_upwards', 'running_downwards', 'at_destination_pos', 'stopped']

    def __init__(self):
        threading.Thread.__init__(self)
        self.amount_of_steps = 0
        self.steps_taken = 0
        self.sm = StateMachine.get_stepperv_machine(self, StepperV._states)
        self.delay = 0.0005
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(21, CW)
        print("[ StepperV ] initialized")

    def run(self):
        # 1. Move down to cargo (running downwards)
        print("[ StepperV ] Direction set to: CW (downwards)")
        print("[ StepperV ] Steps to take: "+str(self.amount_of_steps))
        print("[ StepperV ] ON")
        while int(self.steps_taken) < int(self.amount_of_steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(self.delay)
            self.steps_taken += 1
        print("[ StepperV ] OFF")
        print("[ StepperV ] Steps taken: " + str(self.steps_taken))
        print("[ StepperV ] Waiting for cargo...")
        self.stop_stepperV()

        # 2. Wait at cargo until state changes from main (stopped)
        while self.is_stopped():
            pass

        # 3. Move back up to start position
        self.steps_taken = 0
        print("[ StepperV ] Reset steps taken to 0")
        print("[ StepperV ] Hopefully picked up cargo")
        print("[ StepperV ] ON")

        while int(self.steps_taken) < int(self.amount_of_steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
            self.steps_taken += 1

        print("[ StepperV ] OFF")
        print("[ StepperV ] Steps taken: " + str(self.steps_taken))

        while self.is_stopped():
            pass

        print("[ StepperV ] Resetting steps taken to 0")
        self.steps_taken = 0

        print("[ StepperV ] ON")
        print("[ StepperV ] Steps to take: " + str(self.amount_of_steps))
        while int(self.steps_taken) < int(self.amount_of_steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
            self.steps_taken += 1

        print("[ StepperV ] OFF")
        #self.clean_up()

    def calculate_pos(self):
        pass

    def get_sm(self):
        return self.sm

    @staticmethod
    def set_direction(direction):
        GPIO.output(DIR, direction)
        print("[ StepperV ] Direction: "+str(direction))

    @staticmethod
    def clean_up():
        print("[ StepperV ] GPIO cleanup")
        GPIO.cleanup()
