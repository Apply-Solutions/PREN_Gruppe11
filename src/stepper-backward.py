from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1000   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# set direction forward (clockwise)
GPIO.output(DIR, CW) 

step_count = SPR
delay = .002

if __name__ == '__main__':
    try:
	while True:
	    GPIO.output(STEP, GPIO.HIGH)
	    sleep(delay)
	    GPIO.output(STEP, GPIO.LOW)
	    sleep(delay)
    except KeyboardInterrupt:
	GPIO.output(STEP, GPIO.LOW)
	GPIO.cleanup()
