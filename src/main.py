from BTServer import BluetoothServer
from StepperH import StepperH
from StepperV import StepperV
from ImageProcessor import ImageProcessor
from ElectroMagnet import ElectroMagnet
from StateMachine import StateMachine

_states = ['initialised', 'running', 'stopped']


def add_mainthread_transitions(machine):
    machine.add_transition(trigger='start',
                           source='initialised',
                           dest='running')
    machine.add_transition(trigger='stop',
                           source='running',
                           dest='stopped')


def add_btserver_transitions(machine):
    machine.add_transition(trigger='search',
                           source='initialised',
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
    machine.add_transition(trigger='start',
                           source='initialised',
                           dest='running_forwards')

    machine.add_transition(trigger='change_to_forwards',
                           source='running_forwards',
                           dest='running_backwards')

    machine.add_transition(trigger='stop',
                           source='running_forwards',
                           dest='stopped',
                           after='stepperh_at_position')

    machine.add_transition(trigger='resume_forwards',
                           source='stopped',
                           dest='running_forwards')


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
    machine.add_transition(trigger='start',
                           source='initialising',
                           dest='processing')
    machine.add_transition(trigger='start',
                           source='stopped',
                           dest='processing')

    machine.add_transition(trigger='stop',
                           source='processing',
                           dest='found_square',
                           after='found_destination')


def add_magnet_transitions(machine):
    machine.add_transitions(target='power_on',
                            source='initialised',
                            dest='on')
    machine.add_transitions(target='power_on',
                            source='off',
                            dest='on')

    machine.add_transitions(target='power_off',
                            source='on',
                            dest='off')


class MainThread(object):
    pass

# 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet, Nullpunkt)
# 1. BTServer starten
# 2. BTServer Signal erhalten -> StepperH starten
# 3. Run until StepperH stopped -> StepperV + ElectroMagnet starten
# 4. Wait until StepperV stopped + ImageProcessing start
# 5. Start StepperH
# 6. Run until ImageProcessing state changed
# 7. Wait until StepperV stopped + ImageProcessing stopped


if __name__ == '__main__':
    mainthread = MainThread()

    # 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet, Nullpunkt)
    self_sm = StateMachine.get_main_machine(mainthread, _states)
    server = BluetoothServer()
    stepperH = StepperH()
    stepperV = StepperV()
    imgProcessor = ImageProcessor()
    electroMagnet = ElectroMagnet()
    add_mainthread_transitions(self_sm)
    add_btserver_transitions(server.get_sm())
    add_stepperh_transitions(stepperH.get_sm())
    add_stepperv_transitions(stepperV.get_sm())
    add_imgproc_transitions(imgProcessor.get_sm())

    # 1. BTServer starten
    server.start()

    while mainthread.is_running():
        pass


def server_got_signal():
    stepperH.start()


def stepperh_at_position():
    # TODO: change current position
    stepperV.current_pos = stepperH.get_y()
    stepperV.start()
    electroMagnet.power_on()


def stepperv_at_position():
    if stepperV.has_cargo:
        imgProcessor.start()

    stepperH.resume_forwards()


def found_destination():
    stepperH.stop()

    # TODO: change current position
    stepperV.current_pos = stepperH.get_y()
    stepperV.resume_downwards()


def cargo_at_bay():
    electroMagnet.power_off()
