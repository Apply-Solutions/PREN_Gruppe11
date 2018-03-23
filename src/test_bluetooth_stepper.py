from StepperH import StepperH
from BTServer import BluetoothServer
import time

if __name__ == '__main__':
    server = BluetoothServer()
    stepperH = StepperH()
    print(server.isConnected)
    while not server.isConnected:
        print("waiting for connection to client")
        time.sleep(1)
    while server.hasStartSignal:
        print("waiting for startsignal")
        time.sleep(1)
    stepperH.start()