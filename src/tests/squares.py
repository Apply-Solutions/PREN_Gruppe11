#!/usr/bin/env python

# Python 2/3 compatibility
import sys
import numpy as np
import cv2
import time
import picamera
from picamera.array import PiRGBArray


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


def find_squares(img):
    squares = []

    for gray in cv2.split(img):
        _retval, bin = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and 1000 < cv2.contourArea(cnt) < 70000 and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)

    return squares


if __name__ == '__main__':
    from glob import glob

    #for fn in glob('../data/pic*.jpg'):
    #   img = cv.imread(fn)
    #    squares = find_squares(img)
    #    cv.drawContours(img, squares, -1, (0, 255, 0), 3)
    #    cv.imshow('squares', img)
    #    ch = cv.waitKey()
    #    if ch == 27:
    #        break
    #cv.destroyAllWindows()

    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 10
    camera.exposure_mode = 'sports'

    rawCapture = PiRGBArray(camera)

    # allow the camera to warmup
    time.sleep(0.1)

    print(time.strftime("%d.%m.%Y %H:%M:%S"))
    counter = 0
    while counter < 30:
        camera.capture(rawCapture, format="bgr")

        listOfSquares = find_squares(rawCapture.array)

        if len(listOfSquares) == 0:
            print("No Square found.")
        else:
            print(str(len(listOfSquares)) + " Squares found!!")

        rawCapture.truncate(0)
        counter = counter + 1

    #cv.destroyAllWindows()
    print(time.strftime("%d.%m.%Y %H:%M:%S"))

