#!/usr/bin/env python

# Python 2/3 compatibility
import sys
import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


def find_squares(img):
    squares = []

    for gray in cv.split(img):
        _retval, bin = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)
        bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and 1000 < cv.contourArea(cnt) < 70000 and cv.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)

    return squares


if __name__ == '__main__':
    from glob import glob
    for fn in glob('../data/pic*.jpg'):
        img = cv.imread(fn)
        squares = find_squares(img)
        cv.drawContours(img, squares, -1, (0, 255, 0), 3 )
        cv.imshow('squares', img)
        ch = cv.waitKey()
        if ch == 27:
            break
    cv.destroyAllWindows()
