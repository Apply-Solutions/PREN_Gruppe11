import distance
import RPi.GPIO as GPIO
import time
import BTServer
import math
import StepperHorizontal


def main():
    try:
        while True:
            dist = distance.distance()
            print("Measured Distance = %.1f cm" % dist)

            BTServer.send_message(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "@" + dist)
            time.sleep(1)
    except err:
        print(err)


def start_cat(start_range):

    # set x to null and detect starting position
    send_start_position()
    start_horizontal()
    time.sleep(20)  # maybe with steps instead of just starting motor
    stop_horizontal()

    return "done! YEAH!"


def send_start_position():
    for x in range(0, 5):
        mast_width = 10*10  # (10cm thickness of first mast)
        slope_radiant = math.radiant(8.13)  # 8.13 degrees
        x = distance.distance()
        y = math.tan(slope_radiant) * (distance + mast_width)
        coordinates = [x, y]
        BTServer.sendMessage(coordinates)  # send coordinates to client through server
        time.sleep(1)

    GPIO.cleanup()


def start_horizontal():
    StepperHorizontal.start_motor()


def stop_horizontal():
    StepperHorizontal.stop_motor()


if __name__ == '__main__':
    main()