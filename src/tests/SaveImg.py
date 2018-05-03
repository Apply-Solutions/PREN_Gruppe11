import picamera

if __name__ == '__main__':

    camera = picamera.PiCamera()

    camera.resolution = (320, 240)
    camera.capture("testImage.jpg", resize=(320, 240))
