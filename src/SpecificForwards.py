from SpecificStepperH import StepperH

import time
import sys


def add_stepperv_transitions(machine):
    machine.add_transition(trigger='prepare',
                           source='initialised',
                           dest='running_forwards')

    machine.add_transition(trigger='change_to_forwards',
                           source='running_forwards',
                           dest='running_backwards')
    machine.add_transition(trigger='change_to_backwards',
                           source='running_backwards',
                           dest='running_forwards')

    machine.add_transition(trigger='stop',
                           source='running_forwards',
                           dest='stopped')
    machine.add_transition(trigger='stop',
                           source='running_backwards',
                           dest='stopped')

    machine.add_transition(trigger='resume_forwards',
                           source='stopped',
                           dest='running_forwards')
    machine.add_transition(trigger='resume_backwards',
                           source='stopped',
                           dest='running_backwards')


if __name__ == '__main__':
    stepper = StepperH()
    add_stepperv_transitions(stepper.get_sm())
    stepper.set_direction(0)
    steps = int(sys.argv[1])
    stepper.set_steps(steps)

    try:
	stepper.prepare()
        stepper.start()
        while stepper.is_running_backwards or stepper.is_running_forwards:
	    print("running")
	    time.sleep(2)

	print("Stop")
    except KeyboardInterrupt:
        running = False
        stepper.stop()