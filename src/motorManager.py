import RPi.GPIO as GPIO

def start_motor():
    GPIO.setmode(GPIO.BCM)

    # initialize pin 18 as output pin
    GPIO.setup(18, GPIO.OUT)

    # set pin 18
    pwm = GPIO.PWM(18, 100)

    # the start cycle
    pwm.start(5)


if __name__ == '__main__':
    start_motor()
