from src import StepperHorizontal
import threading


def start_stepper_motor():
    stepper_horizontal = StepperHorizontal()
    try:
        stepper_horizontal.start()
    except(KeyboardInterrupt, SystemExit):
        stepper_horizontal.running = False