from StepperH import StepperH
from ElectroMagnet import ElectroMagnet
import time


# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper = StepperH()
    magnet = ElectroMagnet()

    try:
        stepper.start()
        time.sleep(2.5)
        magnet.start()
        while True:
            pass
    except(KeyboardInterrupt, SystemExit):
        magnet.clean_up()
        stepper.running = False
        # magnet.running = False
