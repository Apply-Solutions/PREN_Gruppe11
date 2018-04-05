import time
from src.ImageProcessor import ImageProcessor

if __name__ == '__main__':
    print ("start")
    img_processor = ImageProcessor()

    print ("start processing")
    img_processor.start()

    while True:
        print(time.strftime("%d.%m.%Y %H:%M:%S"))
        print(img_processor.get_state())