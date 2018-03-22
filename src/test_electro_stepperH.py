from StepperH import StepperH
from ElectroMagnet import ElectroMagnet
import time


# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper = StepperH()
    time.sleep(5)
    magnet = ElectroMagnet()

    try:
        stepper.start()
        time.sleep(10)
        magnet.start()
        while True:
	    print("")
    except(KeyboardInterrupt, SystemExit):
        magnet.clean_up()
        stepper.running = False
        magnet.running = False
