import bluetooth
import sys
import start_cat

# import functions from other files (send position, start function)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 8700
status = "paused"

server_socket.bind(("", 0))
server_socket.listen(1)

print ("Listening on port %d" % port)

uuid = "b9263ab4-2eb9-4792-9472-b20b97f4b2e9"
bluetooth.advertise_service(server_socket, "SampleServer", uuid, [uuid, bluetooth.SERIAL_PORT_CLASS],
                            [bluetooth.SERIAL_PORT_PROFILE])

client_sock, address = server_socket.accept()
print ("Accepted connection from ", address)
client_sock.send("status@" + status + "#")
while True:
    received_data = client_sock.recv(1024) #receiveData here

    if received_data.strip() == "disconnect":
        client_sock.send("dack#") # disconnects client
        received_data = ""
        client_sock.close()
        sys.exit("Received disconnect message. Shutting down server.")

    elif received_data.strip() == "start-process":
        print ("Received message from client: " + received_data)
        received_data = ""
        status = "started"
        client_sock.send("status@" + status + "#")
        # function call here
        start_cat()


def sendMessage():



    return "done"