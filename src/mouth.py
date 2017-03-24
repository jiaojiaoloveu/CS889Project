import cv2
import time

class Mouth:
    def __init__(self):
        self.pos = (-1, -1, -1, -1)
        self.cmdtime = time.time()
        self.threshold = 2

    def update(self, rec):
        curtime = time.time()
        if len(rec) == 0 and curtime - self.cmdtime > self.threshold:
            self.cmdtime = curtime
            return True
        else:
            self.pos = res
            return False
        
