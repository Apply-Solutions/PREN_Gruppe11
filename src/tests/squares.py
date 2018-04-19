#!/usr/bin/env python

# Python 2/3 compatibility
import sys
import numpy as np
import cv2

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


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
                max_cos = np.max(
                    [angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)

    return squares


if __name__ == '__main__':
    from glob import glob

    count = 1
    for fn in glob('../../data/pic*.jpg'):
        img = cv2.imread(fn)
        squares = find_squares(img)

        if len(squares) > 0:
            # calculate center
            x_list = []
            y_list = []

            for square in squares:
                m = cv2.moments(square)
                x_list.append(int(m["m10"] / m["m00"]))
                y_list.append(int(m["m01"] / m["m00"]))

            print reduce(lambda x, y: x + y, x_list) / float(len(x_list))
            print reduce(lambda x, y: x + y, y_list) / float(len(y_list))

            cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
            cv2.imwrite('../../data/pic_edited_' + str(count) + '.jpg', img)
            ch = cv2.waitKey()
            count = count + 1

        if ch == 27:
           break
    cv2.destroyAllWindows()
