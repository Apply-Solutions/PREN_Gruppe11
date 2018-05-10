from StateMachine import StateMachine
from time import sleep
import RPi.GPIO as GPIO

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation (down)
CCW = 0    # Counterclockwise Rotation (up)


class StepperV():
    _states = ['initialized', 'running_upwards', 'running_downwards', 'at_destination_pos', 'stopped']

    def __init__(self):
        # init attributes
        self.steps_taken = 0
        self.delay = 0.0005
        self.sm = StateMachine.get_stepperv_machine(self, StepperV._states)
        # init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(21, CW)
        print("[ StepperV ] initialized")

    def on(self, direction=1, amount_of_steps=0):
        self.steps_taken = 0
        GPIO.output(21, direction)
        print("[ StepperV ] Direction set to: "+str(direction))
        print("[ StepperV ] Steps to take: "+str(amount_of_steps))
        print("[ StepperV ] ON")

        while int(self.steps_taken) < int(amount_of_steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(self.delay)
            self.steps_taken += 1

        print("[ StepperV ] OFF")
        print("[ StepperV ] Steps taken: " + str(self.steps_taken))
        print("[ StepperV ] Waiting for cargo...")

    def stop(self):
        self.stop_stepperV()

    def get_sm(self):
        return self.sm

    @staticmethod
    def clean_up():
        print("[ StepperV ] GPIO cleanup")
        GPIO.cleanup()
