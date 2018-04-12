from bluetooth import *
from random import random
from StateMachine import StateMachine
import datetime
import sys
import threading

server_socket = BluetoothSocket(RFCOMM)
client_sock = ''


class BluetoothServer(threading.Thread):
    _states = ['initialised', 'searching', 'connecting', 'connected', 'waiting', 'running', 'stopped']

    def __init__(self):
        threading.Thread.__init__(self)
        self.isAlive = True
        self.sm = StateMachine.get_bt_server_machine(self, BluetoothServer._states)
        add_transitions(self.sm)
        print("Bluetooth server started")

    def send_message(self, message):
        client_sock.send(message)

    def demo_data(self):
        return random() * 100

    def getDatetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def get_sm(self):
        return self.sm

    def run(self):
        port = 8700
        status = "paused"
        uuid = "00001105-0000-1000-8000-00805f9b34fb"

        # Bind socket and start listening on port
        server_socket.bind(("", 0))
        server_socket.listen(1)

        # Change state to searching
        self.search()

        print("Listening on port %d" % port)

        # Advertise service as available connection
        advertise_service(server_socket, "LaufkatzeT11",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])

        # Wait for incoming connection
        client_sock, client_info = server_socket.accept()

        # Switch state to connect and afterwards to connected
        self.connect()
        self.connected()

        print("Accepted connection from ", client_info)
        client_sock.send("status@" + status + "#")

        # Switch state to waiting_for_start_signal
        self.wait_for_start_signal()

        while self.is_wait_for_start_signal() or self.is_running():
            received_data = client_sock.recv(1024)  # receiveData here

            if received_data.strip() == "disconnect":
                client_sock.send(self.getDatetime() + "@dack" + "#")  # disconnects client
                received_data = ""
                client_sock.close()
                self.stop_server()
                sys.exit("Received disconnect message. Shutting down server.")

            elif received_data.strip() == "start-process":
                print("Received start signal from client. Changing state now...")
                received_data = ""
                status = "started"
                self.start_machine()
