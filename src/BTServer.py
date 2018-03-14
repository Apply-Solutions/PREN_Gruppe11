from bluetooth import *
import datetime
import sys
import start_cat

def send_message(message):
    client_sock.send(message)


def main():
    server_socket = BluetoothSocket(RFCOMM)
    port = 8700
    status = "paused"
    uuid = "b9263ab4-2eb9-4792-9472-b20b97f4b2e9"
    client_sock = ''

    server_socket.bind(("", 0))
    server_socket.listen(1)

    print("Listening on port %d" % port)

    advertise_service( server_socket, "LaufkatzeT11",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
                   )

    address = server_socket.accept()
    print("Accepted connection from ", address)
    client_sock.send("status@" + status + "#")
    while True:
        received_data = client_sock.recv(1024)  # receiveData here

        if received_data.strip() == "disconnect":
            client_sock.send(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@dack")  # disconnects client
            received_data = ""
            client_sock.close()
            sys.exit("Received disconnect message. Shutting down server.")

        elif received_data.strip() == "start-process":
            print("Received message from client: " + received_data)
            received_data = ""
            # function call here
            start_cat.main()
            status = "started"
            client_sock.send(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "status@" + status)

if __name__ == '__main__':
    main()