from StateMachine import StateMachine
import math
import RPi.GPIO as GPIO
import threading
import sys
from time import sleep

DIR = 21  # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
TRIG = 4  # Electromagnet
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 1000  # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)

# set direction forward (clockwise)
GPIO.output(DIR, CCW)

step_count = SPR
delay = .0005


class StepperV(threading.Thread):
    _states = ['initialized', 'running_forwards', 'running_backwards', 'stopped']
    position = [0, 0]

    def __init__(self):
        threading.Thread.__init__(self)
        self.steps = 0;
        self.lastStep = 0;
        self.delay = .0005
        self.count = 5
        self.running = True
        self.sm = StateMachine.get_stepperv_machine(self, StepperV._states)

    def run(self):
        print("\nStepperV ON")
        GPIO.output(TRIG, GPIO.HIGH)

        while self.running:
            self.do_steps()

        print("[ StepperV ] OFF")
        self.clean_up()

    def get_sm(self):
        return self.sm

    def do_steps(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        self.steps = self.steps + 1
        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)
        self.update_position()
        print(self.steps)

    def update_position(self):
        self.position[0] += 1
        self.position[1] += 1

    def set_steps(self, steps):
        self.lastStep = steps

    def set_steps_cm(self, distanceInMili):
        y = distanceInMili/float(10)
        steps = round(-100*(math.sqrt(-1000*(y - 2215.269))-1480), 0)
        self.lastStep = steps

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    @staticmethod
    def set_direction(direction):
        GPIO.output(DIR, direction)
    @staticmethod
    def clean_up():
        print("\nStepperV OFF")
        GPIO.cleanup()

def add_stepperv_transitions(machine):
    machine.add_transition(trigger='prepare',
                           source='initialized',
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


if __name__ == '__main__':
    stepper = StepperV()
    add_stepperv_transitions(stepper.get_sm())
    stepper.set_direction(int(sys.argv[2]))
    stepsInMili = int(sys.argv[1])
    stepper.set_steps_cm(stepsInMili)

    try:
        stepper.prepare()
        stepper.start()
        while stepper.is_running_backwards or stepper.is_running_forwards:
            print("running")
            time.sleep(2)
        print("Stop")
    except KeyboardInterrupt:
        stepper.running = False
        stepper.stop()

