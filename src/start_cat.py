import Distance
import time
import BTServer
import math
import numpy as np
import StepperHorizontal


# if measured distance on first measurements are
# out of start_range start measurements again
def start_cat(start_range):

    # set x to null and detect starting position
    send_start_position()
    start_horizontal()
    time.sleep(20)  # maybe with steps instead of just starting motor
    stop_horizontal()

    return "done! YEAH!"


def send_start_position():

    measurements = []
    mast_width = 10 * 10  # (10cm thickness of first mast)
    slope_radiant = math.radiant(8.13)  # 8.13 degrees

    for n in range(0, 5):
        measurements[n] = Distance.distance()
        time.sleep(1)

    x = np.mean(measurements)
    y = math.tan(slope_radiant) * (x + mast_width)

    try:
        print("Measured Distance From Start Mast= %.1f cm" % x)
        BTServer.send_message(time.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@" + x + ";" + y)
    except Exception:
        print(Exception.message)
        # maybe implement fallback in case sending fails


def start_horizontal():
    StepperHorizontal.start_motor()


def stop_horizontal():
    StepperHorizontal.stop_motor()