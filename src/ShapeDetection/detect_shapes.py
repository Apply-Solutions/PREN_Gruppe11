# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import picamera
from time import sleep

if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    counter = 0
    while True:
        imageName = "pic_imageTest_" + str(counter) + ".jpg"

        camera.capture(imageName, resize=(320, 240))
        img = cv2.imread(imageName)

        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        sd = ShapeDetector()

        # loop over the contours
        for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            shape = sd.detect(c)
            
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c = c.astype("int")
            cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

            if shape == "square":
                print("Square found.")
                
                # show the output image
                cv2.imshow("Image", img)
                cv2.waitKey(0)
            elif shape == "rectangle":
                print("Rectangle found.")
                
                # show the output image
                cv2.imshow("Image", img)
                cv2.waitKey(0)
            else:
                print("No Squares found.")            
            

        counter = counter + 1
        sleep(1)
