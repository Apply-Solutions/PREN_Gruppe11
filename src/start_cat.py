import distance
import RPi.GPIO as GPIO
import time
import BTServer
import math


def start_cat(start_range):

    # set x to null and detect starting position
    send_start_position()
    
    return "done! YEAH!"


def send_start_position():
    for x in range(0,5):
        mast_width = (10)*10 # (10cm thickness of first mast)
        slope_radiant = math.radiant(15) # 15 degrees
        x = distance()
        y = math.tan(slope_radiant) * (distance + mast_width)
        coordinates = [x, y]
        BTServer.sendMessage(coordinates) # send coordinates to client through server
        time.sleep(1)

    GPIO.cleanup()