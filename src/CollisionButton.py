from Observable import Observable
import RPi.GPIO as GPIO
import time
from threading import Thread
from StateMachine import StateMachine

GPIO_ECHO = 18


class CollisionButton(Observable):
    _states = ['initialized', 'running', 'stopped']

    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        # set GPIO Pins

        # set GPIO input (IN / OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        Observable.__init__(self)
        self.sm = StateMachine.get_collision_machine(self, CollisionButton._states)
        print("[ CollisionButton ] Initialized")

    def start_collision_thread(self):
        print("[ CollisionButton ] ON")
        thrd = Thread(target=self.detect_collision, args=())
        thrd.daemon = True
        # start the thread to read frames from the video stream
        self.start_collision()
        thrd.start()
        return self

    def detect_collision(self):
        while self.is_running():
            time.sleep(0.5)
            # print("[ CollisionButton ]" + str(GPIO.input(GPIO_ECHO)))
            if GPIO.input(GPIO_ECHO):
                print("[ CollisionButton ] Collided")
                self.stop_collision()
                Observable.dispatch(self, 'True')

    def get_sm(self):
        return self.sm
