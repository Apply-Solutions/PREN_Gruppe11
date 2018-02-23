# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

# set GPIO Pins
GPIO_TRIGGER = 12

# set GPIO direction (IN / OUT)
PGIO.setup(GPIO_TRIGGER, PGIO.OUT)

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
  except KeyboardInterrupt:
      GPIO.cleanup()
