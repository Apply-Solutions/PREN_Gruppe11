import datetime
import sys
import threading
from random import random
from bluetooth import *

server_socket = BluetoothSocket(RFCOMM)
client_sock = ''


class BluetoothServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.isAlive = True
        self.isConnected = False
        self.isListening = False
        self.hasStartSignal = False
        print("Bluetooth server started")

    def send_message(self, message):
        client_sock.send(message)

    def demo_data(self):
        return random() * 100

    def getDatetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def run(self):
        port = 8700
        status = "paused"
        uuid = "00001105-0000-1000-8000-00805f9b34fb"

        server_socket.bind(("", 0))
        server_socket.listen(1)

        print("Listening on port %d" % port)

        advertise_service(server_socket, "LaufkatzeT11",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE]
                          )

        client_sock, client_info = server_socket.accept()
        print("Accepted connection from ", client_info)
        client_sock.send("status@" + status + "#")

        self.isConnected = True
        self.isListening = True
        while self.isListening:
            received_data = client_sock.recv(1024)  # receiveData here

            if received_data.strip() == "disconnect":
                client_sock.send(self.getDatetime() + "@dack" + "#")  # disconnects client
                received_data = ""
                client_sock.close()
                sys.exit("Received disconnect message. Shutting down server.")

            elif received_data.strip() == "start-process":
                print("Received start signal from client. Changing state now...")
                received_data = ""
                status = "started"
                self.hasStartSignal = True
