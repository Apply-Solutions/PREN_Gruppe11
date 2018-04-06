from time import sleep
import math
import RPi.GPIO as GPIO
import threading

DIR = 24   # Direction GPIO Pin
STEP = 23  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1000   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# set direction forward (clockwise)
GPIO.output(DIR, CCW)

step_count = SPR
delay = .0005


class StepperH(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
	self.breaking = True
	self.delay = 0.05
	self.count = 5

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
