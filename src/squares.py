#!/usr/bin/env python

# Python 2/3 compatibility
import sys
import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


def find_squares2(img):
    ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
    # cv.imshow('Foo2', thresh1)

    edges = cv.Canny(thresh1, 0, 1, apertureSize=3)
    #edges = cv.dilate(edges, None)

    plt.subplot(121), plt.imshow(thresh1, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()


def find_squares(img):
    #img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        _retval, bin = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
    return squares


if __name__ == '__main__':
    from glob import glob
    for fn in glob('../data/pic*.png'):
        img = cv.imread(fn)
        #find_squares2(img)
        squares = find_squares(img)
        cv.drawContours(img, squares, -1, (0, 255, 0), 3 )
        cv.imshow('squares', img)
        ch = cv.waitKey()
        if ch == 27:
            break
    cv.destroyAllWindows()
