from BTServer import BluetoothServer
from StepperH import StepperH
from StepperV import StepperV
from ImageProcessor import ImageProcessor
from ElectroMagnet import ElectroMagnet
from CollisionButton import CollisionButton
from StateMachine import StateMachine
from Observer import Observer
import transition
import time
import multiprocessing


_states = ['initialized', 'running', 'stopped']
server = 0


class MainThread(Observer):

    def __init__(self):
        Observer.__init__(self)
        self.message_number = 0

    def update(self, message):
        if message != 'True':
            if self.message_number > 10:
                server.send_message(server.getDatetime() + "@[ position ];" + message + "#")
            if self.message_number <= 10:
                self.message_number += 1
            else:
                self.message_number = 0
        else:
            print("[ MAIN ] Stopping StepperH because of collision")
            stepperH.running = False

    def stop_stepper_on_collision(self):
        stepperH.stop_running()


# -------------------------------------------------------------------------------------
# 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet, CollisionButton)
# 1. Start BTServer
# 2. BTServer got start signal
# 3. StepperH at cargo position
# 4. StepperV pick up cargo and resume forwards
# 5. StepperH run forwards until square found
# 6. StepperH at drop position -> StepperV drop cargo
# 7. Go to finish line!
# -------------------------------------------------------------------------------------

# Step 0 and 1 at bottom of file

# ------------------------------------------------------------------
# 2. BTServer got start signal
# ------------------------------------------------------------------
def server_got_signal(steps):
    print("[ MAIN ]: BTServer got signal")
    print("[ MAIN ]: Get X, "+str(stepperH.get_x()))
    stepperH.start_stepperH()
    stepperH.run_to_cargo(steps)
    print("[ MAIN ]: StepperH started")


# ------------------------------------------------------------------
# 3. StepperH at cargo position
# ------------------------------------------------------------------
def stepperh_at_position():
    # TODO: change current position
    server.send_message(server.getDatetime() + "@[ StepperH ] At pos#")
    print("[ MAIN ] stepperh_at_position()")
    print("[ MAIN ] Set StepperV amount of steps to take: "+str(stepperH.get_y()))

    stepperV.start_stepperV() # State Change
    stepperV.on(int(1), int(stepperH.get_y()))

    server.send_message(server.getDatetime() + "@[ Electromagnet ] Turning on...#")
    electroMagnet.on()

    stepperV.stop_stepperV() # State Change


# ------------------------------------------------------------------
# 4. StepperV pick up cargo and resume forwards
# ------------------------------------------------------------------
def stepperv_at_position():
    print("[ MAIN ] stepperv_at_position()")
    server.send_message(server.getDatetime() + "@[ event ] Cargo picked up#")
    time.sleep(1)

    print("[ MAIN ] Amount of steps for StepperV = "+str(stepperH.get_y()))
    stepperV.on(int(0), int(stepperH.get_y()))

    print("[ MAIN ] Starting Image Processor...")
    server.send_message(server.getDatetime() + "@[ ImageProcessor ] Starting image processor...#")
    imgProcessor.start_imgproc()
    imgProcessor.start()

    print("[ MAIN ] StepperH resume forwards")
    server.send_message(server.getDatetime() + "@[ StepperH ] Resuming forwards#")
    stepperH.resume_forwards() # State Change to running_forwards
    stepperH.run_until_stopped()
    imgProcessor.stop_imgproc()


# ------------------------------------------------------------------
# 5. StepperH run forwards until square found
# ------------------------------------------------------------------
def running_forwards():
    print("[ MAIN ] running_forwards()")


# ------------------------------------------------------------------
# 6. StepperH at drop position -> StepperV drop cargo
# ------------------------------------------------------------------
def found_destination():
    server.send_message(server.getDatetime() + "@[ ImageProcessor ] Found destination#")
    print("[ MAIN ] fount_destination()")
    print("[ MAIN ] Attempting to stop Image Processor")
    imgProcessor.stop()
    print("[ MAIN ] Attempting to stop StepperH")

    stepperH.running = False
    stepperH.on()
    # Stepper going down to drop cargo
    print("[ MAIN ] Resuming StepperV")
    server.send_message(server.getDatetime() + "@[ StepperV ] Resuming...#")
    stepperV.on(int(1), stepperH.get_y())
    stepperV.resume_downwards()
    electroMagnet.off()  # Drop cargo
    server.send_message(server.getDatetime() + "@[ event ] Cargo at destination#")

    # ------------------------------------------------------------------
    # 7. Go to finish line
    # ------------------------------------------------------------------
    stepperV.on(int(0), stepperH.get_y()) # Resume upwards
    collisionButton.start_collision()
    collisionButton.start()
    stepperH.run_until_collided(collisionButton)
    server.send_message(server.getDatetime() + "@[ event ] Collision detected#")
    server.send_message(server.getDatetime() + "@[ main ] You have reached your final destination#")
    print
    print
    print
    print("[ MAIN ] ------------------------------------------------------------------------------")
    print("[ MAIN ] Final stats:")
    print("[ MAIN ] ------------------------------------------------------------------------------")
    print("[ MAIN ] Steps taken by StepperH: N/A")
    print("[ MAIN ] Time passed until arrived: N/A")
    print("[ MAIN ] Average skill level: 1'000'000!")
    print("[ MAIN ] Final costs for development: CHF 500.-")
    print("[ MAIN ] ------------------------------------------------------------------------------")
    print
    print
    print


if __name__ == '__main__':
    try:
        # ------------------------------------------------------------------
        # 0. Initialising (BTServer, Steppers, ImageProcessor, ElectroMagnet)
        # ------------------------------------------------------------------
        mainthread = MainThread()
        self_sm = StateMachine.get_main_machine(mainthread, _states)
        server = BluetoothServer()

        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()

        stepperH = StepperH(results)
        stepperV = StepperV()
        imgProcessor = ImageProcessor(tasks, results)
        electroMagnet = ElectroMagnet()
        collisionButton = CollisionButton(tasks, results)

        # Add transitions
        transition.add_mainthread_transitions(self_sm)
        transition.add_btserver_transitions(server.get_sm())
        transition.add_stepperh_transitions(stepperH.get_sm())
        transition.add_stepperv_transitions(stepperV.get_sm())
        transition.add_magnet_transitions(electroMagnet.get_sm())
        transition.add_imgproc_transitions(imgProcessor.get_sm())
        transition.add_collision_button_transitions(collisionButton.get_sm())

        # Dynamically add methods
        server.server_got_signal = server_got_signal
        stepperH.stepperh_at_position = stepperh_at_position
        stepperV.stepperv_at_position = stepperv_at_position
        imgProcessor.found_destination = found_destination

        # Register self to Observer
        print("[ MAIN ] Registering StepperH to Observer")
        stepperH.register(mainthread)

        mainthread.start_mt()

        print("[ MAIN ] Starting bluetooth server")

        # ------------------------------------------------------------------
        # 1. Start BTServer
        # ------------------------------------------------------------------
        server.start_thread()
        # -> Next step at method 2. server_got_signal

        print("[ MAIN ] Started bluetooth server")

        while mainthread.is_running():
            time.sleep(2)
    except KeyboardInterrupt:
        print("[ MAIN ] Switching off program!")
        try:
            print("[ MAIN ] Attempting to switch off ImageProcessor")
            imgProcessor.stop()
            imgProcessor.terminate()

            print("[ MAIN ] Attempting to switch off ElectroMagnet")
            electroMagnet.off()
            print("[ MAIN ] Attempting to switch off StepperH")
            stepperH.stop_running()
            print("[ MAIN ] Attempting to switch off MainThread")
            mainthread.stop_running()
            print("[ MAIN ] Attempting to switch off CollisionButton")
            collisionButton.stop_collision()
            collisionButton.terminate()

        except Exception:
            print("[ MAIN ] Failed to stop program correctly...OFF and OUT!")