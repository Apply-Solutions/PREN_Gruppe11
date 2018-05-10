# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 4

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

def magnet():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)

    print("On")

    time.sleep(5000)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    print("Off")


if __name__ == '__main__':
  try:
    while True:
        print("sucking...")
	magnet()
  except KeyboardInterrupt:
      GPIO.cleanup()
