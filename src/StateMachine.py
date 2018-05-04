from transitions.extensions import LockedMachine as Machine


class StateMachine:
    _main_machine = None
    _bt_server_machine = None
    _stepperh_machine = None
    _stepperv_machine = None
    _magnet_machine = None
    _camera_machine = None

    @staticmethod
    def get_main_machine(model, states):
        if StateMachine._main_machine is None:
            StateMachine._main_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._main_machine

    @staticmethod
    def get_bt_server_machine(model, states):
        if StateMachine._bt_server_machine is None:
            StateMachine._bt_server_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._bt_server_machine

    @staticmethod
    def get_stepperh_machine(model, states):
        if StateMachine._stepperh_machine is None:
            StateMachine._stepperh_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._stepperh_machine

    @staticmethod
    def get_stepperv_machine(model, states):
        if StateMachine._stepperv_machine is None:
            StateMachine._stepperv_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._stepperv_machine

    @staticmethod
    def get_magnet_machine(model, states):
        if StateMachine._magnet_machine is None:
            StateMachine._magnet_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._magnet_machine

    @staticmethod
    def get_camera_machine(model, states):
        if StateMachine._camera_machine is None:
            StateMachine._camera_machine = Machine(model=model, states=states, initial='initialized')

        return StateMachine._camera_machine