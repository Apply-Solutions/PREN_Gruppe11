import numpy as np
import cv2
import picamera
import time
from picamera.array import PiRGBArray
from threading import Thread
import ImageProcessor


if __name__ == '__main__':
    print ("start")
    img_processor = ImageProcessor.ImageProcessor()

    print ("start processing")
    img_processor.start()

    count = 0

    print(time.strftime("%d.%m.%Y %H:%M:%S"))
    while count < 10:
        print(img_processor.get_state())
        count = count + 1
        time.sleep(0.5)

    print(time.strftime("%d.%m.%Y %H:%M:%S"))
    img_processor.stop()


class ImageProcessor(object):
    is_where_found = False

    delay_in_sec = 0.1

    def __init__(self):

        resolution = (320, 240)
        framerate = 32

        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.exposure_mode = 'sports'

        self.rawCapture = PiRGBArray(self.camera, resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr", use_video_port=True)

        self.stopped = False
        is_where_found = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.check_if_square, args=()).start()
        return self

    def get_state(self):
        return self.is_where_found

    def stop(self):
        self.stopped = True

    def check_if_square(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

            list_of_squares = self.find_squares(f.array)

            self.rawCapture.truncate(0)

            if len(list_of_squares) == 0:
                self.is_where_found = False
            else:
                self.is_where_found = True

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