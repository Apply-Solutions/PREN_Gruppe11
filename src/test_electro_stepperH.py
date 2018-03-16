from src.StepperH import StepperH
from src.ElectroMagnet import ElectroMagnet
import time


# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper = StepperH()
    magnet = ElectroMagnet()

    try:
        stepper.start()
        time.sleep(3)
        magnet.start()
        while True:
            print('stepper running')
            time.sleep(5)
    except(KeyboardInterrupt, SystemExit):
        stepper.running = False
        stepper.join()
        magnet.running = False
        magnet.join()