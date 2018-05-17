import numpy as np
import cv2
import picamera
import time
from picamera.array import PiRGBArray
from threading import Thread
from StateMachine import StateMachine
from multiprocessing import Process, Value


class ImageProcessor:
    _states = ['initialized', 'processing', 'found_square']
    delay_in_sec = 0.3

    def __init__(self, has_found):
        resolution = (320, 240)
        framerate = 10

        self.has_found = has_found

        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        self.process = None

        self.rawCapture = PiRGBArray(self.camera, resolution)

        self.is_processing = True

        self.sm = StateMachine.get_camera_machine(self, ImageProcessor._states)

        self.is_where_found = False
        self.center_x = 0
        self.center_y = 0
        print("[ ImageProcessor ] initialized")

    def start_thread(self):
        print("[ ImageProcessor ]  enter start thread")
        self.start_imgproc()
        print("[ ImageProcessor ]  start process")
        print("[ ImageProcessor ]  has_found: " + str(self.has_found.value))
        self.process = Process(target=self.run, args=(self.has_found,))
        self.process.start()

        print("[ ImageProcessor ]  process started.")

        return self

    def stop_image_processor(self):
        self.process.stop()
        self.is_processing = False

    def get_state(self):
        return self.is_where_found

    def get_sm(self):
        return self.sm

    def get_center_x(self):
        return self.center_x

    def get_center_y(self):
        return self.center_y

    def run(self, has_found):
        # keep looping infinitely until the thread is stopped
        count = 1

        with PiRGBArray(self.camera) as output:
            while self.is_processing or count > 20:
                count += 1

                self.camera.capture(output, 'rgb', use_video_port=True)
                frame = output.array
                list_of_squares = self.find_squares(frame)

                output.truncate(0)
                print("[ ImageProcessor ] Length: len(list_of_squares) ")
                if len(list_of_squares) == 0:
                    self.is_where_found = False
                else:
                    print("[ ImageProcessor ] Square found")
                    # calculate center
                    x_list = []
                    y_list = []

                    for square in list_of_squares:
                        m = cv2.moments(square)
                        x_list.append(int(m["m10"] / m["m00"]))
                        y_list.append(int(m["m01"] / m["m00"]))

                    self.center_x = reduce(lambda x, y: x + y, x_list) / float(len(x_list))
                    self.center_y = reduce(lambda x, y: x + y, y_list) / float(len(y_list))

                    print("[ ImageProcessor ] Set state.")
                    print("[ ImageProcessor ] X: "+str(self.get_center_x()))
                    self.is_where_found = True
                    self.stop_imgproc()
                    self.is_processing = False
                    has_found.value = True
                    print("[ ImageProcessor ] Processing stopped")

                time.sleep(self.delay_in_sec)

    @staticmethod
    def find_squares(img):
        squares = []

        for gray in cv2.split(img):
            _retval, bin_image = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            bin_image, contours, _hierarchy = cv2.findContours(bin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and 1000 < cv2.contourArea(cnt) < 70000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([ImageProcessor.angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)

        return squares

    @staticmethod
    def angle_cos(p0, p1, p2):
        d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
        return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))
