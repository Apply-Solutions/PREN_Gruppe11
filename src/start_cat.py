import Distance
import time
import BTServer
import math
import numpy as np
import StepperHorizontal
import StepperVertical
import ImageProcessor
import cv2
import picamera
from time import sleep

steps = 0


# if measured distance on first measurements are
# out of start_range start measurements again
def start_cat(start_range):

    # set x to null and detect starting position
    while not send_start_position():
        print("searching distance")
        time.sleep(.5)

    start_horizontal()
    ImageProcessor.status = "ON"

    while not ImageProcessor.status == "ON":
        print("Checking for squares")

        time.sleep(.5)

    # IDEA: If stop, then take so many steps, then stop
    StepperHorizontal.stop_motor(steps)
    stop_image_processing()
    start_vertical()

    return "done! YEAH!"


def send_start_position():

    measurements = []
    mast_width = 10 * 10  # (10cm thickness of first mast)
    slope_radiant = math.radiant(8.13)  # 8.13 degrees

    for n in range(0, 5):
        measurements[n] = Distance.distance()
        time.sleep(1)

    x = np.mean(measurements) * 10
    y = math.tan(slope_radiant) * (x + mast_width) * 10

    try:
        print("Measured Distance From Start Mast= %.1f mm" % x)
        BTServer.send_message(time.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@Position;" + x + ";" + y)
        return True
    except Exception:
        print(Exception.message)
        return False


def check_for_squares():
    # This method is just for test purposes
    ImageProcessor.status == "ON"
    image_name = "image_from_processor.jpg"
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)

    camera.capture(image_name, resize=(320, 240))
    img = cv2.imread(image_name)

    list_of_squares = ImageProcessor.find_squares(img);

    if len(list_of_squares) == 0:
        print("No Square found.")
        return False
    else:
        print(str(len(list_of_squares)) + " Squares found!!")
        return True;


def stop_image_processing():
    ImageProcessor.status = "OFF";


# Maybe change to one program and
# just pass the specific motor
def start_horizontal():
    StepperHorizontal.start_motor()


def start_vertical():
    StepperVertical.start_motor()


def stop_vertical():
    StepperVertical.status = "OFF"