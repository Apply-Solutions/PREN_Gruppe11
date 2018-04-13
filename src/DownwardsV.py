from src import StepperV


def add_stepperv_transitions(machine):
    machine.add_transition(trigger='start',
                           source='initialised',
                           dest='running_upwards')

    machine.add_transition(trigger='change_to_upwards',
                           source='running_upwards',
                           dest='running_downwards')
    machine.add_transition(trigger='change_to_downwards',
                           source='running_downwards',
                           dest='running_upwards')

    machine.add_transition(trigger='stop',
                           source='running_upwards',
                           dest='stopped',
                           after='stepperv_at_position')
    machine.add_transition(trigger='stop',
                           source='running_downwards',
                           dest='stopped')

    machine.add_transition(trigger='resume_upwards',
                           source='stopped',
                           dest='running_upwards')
    machine.add_transition(trigger='resume_downwards',
                           source='stopped',
                           dest='running_downwards')


if __name__ == '__main__':
    stepper = StepperV()
    add_stepperv_transitions(stepper.get_sm())

    try:
        stepper.start()
    except KeyboardInterrupt:
        stepper.stop()
