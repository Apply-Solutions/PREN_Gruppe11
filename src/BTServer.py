from bluetooth import *
from random import random
from StateMachine import StateMachine
import datetime
import sys
import threading

server_socket = BluetoothSocket(RFCOMM)


class BluetoothServer(threading.Thread):
    _states = ['initialised', 'searching', 'connecting', 'connected', 'waiting', 'running', 'stopped']

    __client_sock__ = ''

    def __init__(self):
        threading.Thread.__init__(self)
        self.isAlive = True
        self.sm = StateMachine.get_bt_server_machine(self, BluetoothServer._states)
        print("Bluetooth server started")

    def send_message(self, message):
        self.__client_sock__.send(message)

    def demo_data(self):
        return str(random() * 100)

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
        self.__client_sock__, client_info = server_socket.accept()

        # Switch state to connect and afterwards to connected
        self.connect()
        self.connected()

        print("Accepted connection from ", client_info)
        self.__client_sock__.send("status@" + status + "#")

        # Switch state to waiting_for_start_signal
        self.wait_for_start_signal()

        while self.is_waiting() or self.is_running():
            received_data = self.__client_sock__.recv(1024)  # receiveData here

            if received_data.strip() == "disconnect":
                self.__client_sock__.send(self.getDatetime() + "@dack" + "#")  # disconnects client
                received_data = ""
                self.__client_sock__.close()
                self.stop_server()
                sys.exit("Received disconnect message. Shutting down server.")

            elif received_data.strip() == "start-process":
                print("Received start signal from client. Changing state now...")
                received_data = ""
                status = "started"
                self.start_machine()
