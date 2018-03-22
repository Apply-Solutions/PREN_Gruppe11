from StepperV import StepperV
import time


if __name__ == '__main__':
    stepper = StepperV()
    try:
	stepper.start()
	while True:
	    print('stepper running')
	    time.sleep(2)
    except(KeyboardInterrupt, SystemExit):
	stepper.running = False


