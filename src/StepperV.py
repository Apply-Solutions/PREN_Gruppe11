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

# set direction forward (clockwise)
GPIO.output(DIR, CW)

step_count = SPR
delay = .0005 #in seconds (.005 = 5ms)


def add_transitions(machine):
    machine.add_transition(trigger='start',
                           source='initialised',
                           dest='running_upwards')

    machine.add_transition(trigger='change_to_upwards',
                           source='running_upwards',
                           dest='running_downwards')
    machine.add_transition(trigger='change_to_downwards',
                           source='running_downwards',
                           dest='running_upwards')

    machine.add_transition(trigger='stop',
                           source='running_upwards',
                           dest='stopped')
    machine.add_transition(trigger='stop',
                           source='running_downwards',
                           dest='stopped')

    machine.add_transition(trigger='resume_upwards',
                           source='stopped',
                           dest='running_upwards')
    machine.add_transition(trigger='resume_downwards',
                           source='stopped',
                           dest='running_downwards')


class StepperV(threading.Thread):
    _states = ['initialised', 'running_upwards', 'running_downwards', 'stopped']

    def __init__(self):
        threading.Thread.__init__(self)
        self.sm = StateMachine.get_stepperh_machine(self, StepperV._states)
        add_transitions(self.sm)

    def run(self):
        print("\nStepperV ON")
        while not self.is_stopped():
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

    def clean_up(self):
        print("\nStepperV OFF")
