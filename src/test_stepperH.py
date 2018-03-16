from StepperH import StepperH
import time

# starts horizontal stepper as thread
if __name__ == '__main__':
	stepper = StepperH()
	try:
		stepper.start()
		while True:
			print('stepper running')
			time.sleep(2)
	except(KeyboardInterrupt, SystemExit):
		stepper.running = False
		stepper.join()
