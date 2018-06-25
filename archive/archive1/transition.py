def add_mainthread_transitions(machine):
    machine.add_transition(trigger='start_mt',
                           source='initialized',
                           dest='running')
    machine.add_transition(trigger='stop_running',
                           source='running',
                           dest='stopped')


def add_btserver_transitions(machine):
    machine.add_transition(trigger='search',
                           source='initialized',
                           dest='searching')
    machine.add_transition(trigger='connect',
                           source='searching',
                           dest='connecting')
    machine.add_transition(trigger='connected',
                           source='connecting',
                           dest='connected')
    machine.add_transition(trigger='wait_for_start_signal',
                           source='connected',
                           dest='waiting')
    machine.add_transition(trigger='start_machine',
                           source='waiting',
                           dest='running',
                           after='server_got_signal')
    machine.add_transition(trigger='stop_server',
                           source='*',
                           dest='stopped')


def add_stepperh_transitions(machine):
    machine.add_transition(trigger='start_stepperH',
                           source='initialized',
                           dest='running_forwards')

    machine.add_transition(trigger='change_to_forwards',
                           source='running_forwards',
                           dest='running_backwards')

    machine.add_transition(trigger='stop_stepperH',
                           source='running_forwards',
                           dest='stopped',
                           after='stepperh_at_position')

    machine.add_transition(trigger='resume_forwards',
                           source='stopped',
                           dest='running_forwards')


def add_stepperv_transitions(machine):
    machine.add_transition(trigger='start_stepperV',
                           source='initialized',
                           dest='running_downwards')

    machine.add_transition(trigger='change_to_downwards',
                           source='running_upwards',
                           dest='running_downwards')
    machine.add_transition(trigger='change_to_upwards',
                           source='running_downwards',
                           dest='running_upwards')

    machine.add_transition(trigger='stop_stepperV',
                           source='running_downwards',
                           dest='stopped',
                           after='stepperv_at_position')

    machine.add_transition(trigger='stop_stepperV',
                           source='running_upwards',
                           dest='stopped')

    machine.add_transition(trigger='send_at_position_signal',
                           source='running_downwards',
                           dest='at_destination_pos',
                           after='cargo_at_bay')

    machine.add_transition(trigger='resume_upwards',
                           source='stopped',
                           dest='running_upwards')

    machine.add_transition(trigger='resume_downwards',
                           source='stopped',
                           dest='running_downwards')


def add_imgproc_transitions(machine):
    machine.add_transition(trigger='start_imgproc',
                           source='initialized',
                           dest='processing')
    machine.add_transition(trigger='start_imgproc',
                           source='stopped',
                           dest='processing')

    machine.add_transition(trigger='stop_imgproc',
                           source='processing',
                           dest='found_square',
                           after='found_destination')


def add_magnet_transitions(machine):
    machine.add_transition(trigger='power_on',
                            source='initialized',
                            dest='on')
    machine.add_transition(trigger='power_on',
                            source='off',
                            dest='on')

    machine.add_transition(trigger='power_off',
                            source='on',
                            dest='off')


def add_collision_button_transitions(machine):
    machine.add_transition(trigger="start_collision",
                           source="initialized",
                           dest="running")
    machine.add_transition(trigger="stop_collision",
                           source="running",
                           dest="stopped")