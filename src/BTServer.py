from bluetooth import *
from random import random
import datetime
import start_cat
import sys

server_socket = BluetoothSocket(RFCOMM)
client_sock = ''

def send_message(message):
    client_sock.send(message)

def demo_data():
    return random() * 100

def main():
    port = 8700
    status = "paused"
    uuid = "00001105-0000-1000-8000-00805f9b34fb"

    server_socket.bind(("", 0))
    server_socket.listen(1)

    print("Listening on port %d" % port)

    advertise_service( server_socket, "LaufkatzeT11",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ]
                       )


    client_sock, client_info = server_socket.accept()
    print("Accepted connection from ", client_info)
    client_sock.send("status@" + status + "#")
    while True:
        received_data = client_sock.recv(1024)  # receiveData here

        if received_data.strip() == "disconnect":
            client_sock.send(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@dack" + "#")  # disconnects client
            received_data = ""
            client_sock.close()
            sys.exit("Received disconnect message. Shutting down server.")

        elif received_data.strip() == "start-process":
            print("Received message from client: " + received_data)
            received_data = ""
            # function call here
            start_cat.start_cat(0)
            status = "started"

            x = demo_data()
            y = demo_data()
            print(client_sock)
            client_sock.send(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@Position;" + str(x) + ";" + str(y) + "#")
            # client_sock.send("HELLO")

if __name__ == '__main__':
    main()