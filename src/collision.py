# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, GPIO.HIGH)

def collision():
    
    input = GPIO.input(GPIO_ECHO)

    if input == 1:
	print('collision')
    elif input == 0: 
	print('waiting for input...')    


if __name__ == '__main__':
    try:
        while True:
            collision()
            time.sleep(2)

            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
