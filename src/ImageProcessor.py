import numpy as np
import cv2
import picamera
import time
from picamera.array import PiRGBArray
from threading import Thread
from StateMachine import StateMachine
import multiprocessing


class ImageProcessor(multiprocessing.Process):
    _states = ['initialized', 'processing', 'found_square']
    delay_in_sec = 0.3

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

        self.is_processing = True;

        self.sm = StateMachine.get_camera_machine(self, ImageProcessor._states)

        self.center_x = 0
        print("[ ImageProcessor ] initialized")

    def stop(self):
        self.is_processing = False

    def get_sm(self):
        return self.sm

    def get_center_x(self):
        return self.center_x

    def run(self):
        resolution = (320, 240)

        camera = picamera.PiCamera()
        camera.resolution = resolution
        camera.framerate = 10

        self.result_queue.put("[ ImageProcessor ] started")
        with PiRGBArray(camera) as output:
            # keep looping infinitely until the thread is stopped
            while self.is_processing:

                camera.capture(output, 'rgb', use_video_port=True)
                frame = output.array
                list_of_squares = self.find_squares(frame)

                output.truncate(0)

                if len(list_of_squares)> 0:
                    # calculate center
                    x_list = []

                    for square in list_of_squares:
                        m = cv2.moments(square)
                        x_list.append(int(m["m10"] / m["m00"]))

                    self.center_x = reduce(lambda x, y: x + y, x_list) / float(len(x_list))

                    print("[ ImageProcessor ] Set state.")

                    self.result_queue.put(True)
                    self.stop()
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
