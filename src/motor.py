import RPi.GPIO as GPIO
import time

def start_motor():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 50)
    pwm.start(10)
    
    while 1:
      
        time.sleep(1)
       
if __name__== '__main__':
    start_motor()
