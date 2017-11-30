import RPi.GPIO as GPIO

def start_motor():
    GPIO.setmode(GPIO.BCM)

    # initialize pin 12 as output pin
    GPIO.setup(12, GPIO.OUT)

    # set pin 12
    pwm = GPIO.PWM(12, 100)

    # the start cycle
    pwm.start(5)


if __name__ == '__main__':
    start_motor()
