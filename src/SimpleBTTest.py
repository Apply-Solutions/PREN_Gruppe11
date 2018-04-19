from BTServer import BluetoothServer


def add_btserver_transitions(machine):
    machine.add_transition(trigger='search',
                           source='initialised',
                           dest='searching',
                           after='test')
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
                           after='test.server_got_signal')
    machine.add_transition(trigger='stop_server',
                           source='*',
                           dest='stopped')


def test():
    print("Server idling until connection request")


def server_got_signal():
    print("Server received start signal")


if __name__ == '__main__':
    btserver = BluetoothServer()
    add_btserver_transitions(btserver.get_sm())
    btserver.test = test
    btserver.server_got_signal = server_got_signal
    btserver.start()
