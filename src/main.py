from BTServer import BluetoothServer
from StepperH import StepperH
from StepperV import StepperV
from ImageProcessor import ImageProcessor
from ElectroMagnet import ElectroMagnet
from StateMachine import StateMachine
from Observer import Observer
import time

_states = ['initialized', 'running', 'stopped']
server = 0


def add_mainthread_transitions(machine):
    machine.add_transition(trigger='start',
                           source='initialized',
                           dest='running')
    machine.add_transition(trigger='stop',
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


class MainThread(Observer):

    def __init__(self):
        Observer.__init__(self)
        self.message_number = 0

    def update(self, message):
        if self.message_number > 10:
            server.send_message(server.getDatetime() + "@[ position ];" + message + "#")
        if self.message_number <= 10:
            self.message_number += 1
        else:
            self.message_number = 0

# 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet, Nullpunkt)
# 1. BTServer starten
# 2. BTServer Signal erhalten -> StepperH starten
# 3. Run until StepperH stopped -> StepperV + ElectroMagnet starten
# 4. Wait until StepperV stopped + ImageProcessing start
# 5. Start StepperH
# 6. Run until ImageProcessing state changed
# 7. Wait until StepperV stopped + ImageProcessing stopped


# 2. BTServer got signal from client -> start StepperH
def server_got_signal(steps):
    print("[ MAIN ]: BTServer got signal")
    print("[ MAIN ]: Get X, "+str(stepperH.get_x()))
    stepperH.start_stepperH()
    stepperH.run_to_cargo(steps)
    print("[ MAIN ]: StepperH started")


# 3. StepperH at position
def stepperh_at_position():
    # TODO: change current position
    print("[ MAIN ] stepperh_at_position()")
    print("[ MAIN ] Set StepperV amount of steps to take: "+str(stepperH.get_y()))

    stepperV.start_stepperV() # State Change
    stepperV.on(int(1), int(stepperH.get_y()))

    electroMagnet.on()

    stepperV.stop_stepperV() # State Change


# 4. Get cargo, StepperV move up, Start ImageProcessing, -> Start StepperH
def stepperv_at_position():
    print("[ MAIN ] stepperv_at_position()")
    time.sleep(2)

    print("[ MAIN ] Amount of steps for StepperV = "+str(stepperH.get_y()))
    time.sleep(5)
    stepperV.on(int(0), int(stepperH.get_y()))

    print("[ MAIN ] Starting Image Processor...")
    imgProcessor.start_thread()

    print("[ MAIN ] StepperH resume forwards")
    stepperH.resume_forwards() # State Change to running_forwards
    stepperH.run_until_stopped()


def running_forwards():
    # Wait until ImageProcessor found square and changes state
    print("[ MAIN ] running_forwards()")


def found_destination():
    print("[ MAIN ] fount_destination()")
    print("[ MAIN ] Attempting to stop Image Processor")
    imgProcessor.stop()
    print("[ MAIN ] Attempting to stop StepperH")
    stepperH.running = False

    # TODO: change current position
    print("[ MAIN ] Resuming StepperV")
    stepperV.on(int(1), stepperH.get_y())
    stepperV.resume_downwards()

    electroMagnet.off()

    stepperV.on(int(0), stepperH.get_y())

    stepperH.run_until_stopped()


def cargo_at_bay():
    electroMagnet.power_off()


if __name__ == '__main__':
    try:
        mainthread = MainThread()

        # 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet, Nullpunkt)
        self_sm = StateMachine.get_main_machine(mainthread, _states)
        server = BluetoothServer()

        stepperH = StepperH()
        stepperV = StepperV()
        imgProcessor = ImageProcessor()
        electroMagnet = ElectroMagnet()

        # Register self to Observer
        stepperH.register(mainthread)

        # Add transitions
        add_mainthread_transitions(self_sm)
        add_btserver_transitions(server.get_sm())
        add_stepperh_transitions(stepperH.get_sm())
        add_stepperv_transitions(stepperV.get_sm())
        add_magnet_transitions(electroMagnet.get_sm())
        add_imgproc_transitions(imgProcessor.get_sm())

        # Dynamically add methods
        server.server_got_signal = server_got_signal
        stepperH.stepperh_at_position = stepperh_at_position
        stepperV.stepperv_at_position = stepperv_at_position
        stepperV.cargo_at_bay = cargo_at_bay
        imgProcessor.found_destination = found_destination

        # 1. BTServer starten
        server.start()
        # -> Next step at method server_got_signal

        while mainthread.is_running():
            pass
    except KeyboardInterrupt:
        stepperH.stop_running()
