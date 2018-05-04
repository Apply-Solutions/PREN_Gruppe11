import numpy as np
import cv2
import picamera
import time
from picamera.array import PiRGBArray
from threading import Thread
from StateMachine import StateMachine


class ImageProcessor:
    _states = ['initialized', 'processing', 'found_square']
    delay_in_sec = 0.1

    def __init__(self):
        resolution = (320, 240)
        framerate = 10

        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        self.rawCapture = PiRGBArray(self.camera, resolution)
        #self.stream = self.camera.capture_continuous(self.rawCapture,
        #                                             format="bgr", use_video_port=True)

        #self.frame = None

        self.is_processing = True;

        self.sm = StateMachine.get_camera_machine(self, ImageProcessor._states)

        self.is_where_found = False
        self.center_x = 0
        self.center_y = 0
        print("[ ImageProcessor ] initialized")

    def start_thread(self):
        self.start_imgproc()
        # start the thread to read frames from the video stream
        Thread(target=self.check_if_square, args=()).start()
        return self

    def stop(self):
        self.is_processing = False;

    def get_state(self):
        return self.is_where_found

    def get_sm(self):
        return self.sm

    def get_center_x(self):
        return self.center_x

    def get_center_y(self):
        return self.center_y

    def check_if_square(self):
        # keep looping infinitely until the thread is stopped
        count = 1
        #for f in self.stream:
        with PiRGBArray(self.camera) as output:
            while self.is_processing:

                # if not self.is_processing():
                #     self.stream.close()
                #     self.rawCapture.close()
                #     self.camera.close()
                #     return
                #
                # self.frame = f.array

                self.camera.capture(output, 'rgb', use_video_port=True)
                frame = output.array
                list_of_squares = self.find_squares(frame)
                #self.rawCapture.truncate(0)


                # save image to debug
                cv2.drawContours(frame, list_of_squares, -1, (0, 255, 0), 3)
                cv2.imwrite('../../data/pic_edited_' + str(count) + '.jpg', frame)
                count = count + 1

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
                    self.is_where_found = True
                    self.stop_imgproc()
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
