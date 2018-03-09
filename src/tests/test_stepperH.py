from src import StepperH


# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper_h = StepperH()
    try:
        stepper_h.start()
        while True:
            print('stepper running')
    except(KeyboardInterrupt, SystemExit):
        stepper_h.running = False
        stepper_h.join()