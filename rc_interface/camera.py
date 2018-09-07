from threading import Thread
import time

from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (239, 160)
        self.filming = False
        self.sequence = 0
        self.threads = list()

    def snap(self):
        self.filming = True
        while self.filming:
            image_name = 'car1_{}_{}.jpg'.format(self.sequence,
                                                 int(time.time()))
            self.camera.capture(image_name)
            time.sleep(1)

    def open(self):
        self.sequence += 1
        self.filming = True
        t = Thread(target=self.snap)
        t.start()

    def closed(self):
        self.filming = False
