from BTServer import BluetoothServer

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


if __name__=='__main__':
    btserver = BluetoothServer()
    add_btserver_transitions(btserver.get_sm())
    btserver.start()