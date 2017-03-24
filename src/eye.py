import cv2
import time

class Eye:
    def __init__(self):
        self.pos = (-1, -1, -1, -1)
        self.cmdtime = time.time()
        self.nortime = time.time()
        self.threshold = 1

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def update(self, alpos, pos):
        curtime = time.time()
        if len(alpos) > 0:
            if len(pos) == 0:
                if self.cmdtime > self.nortime:
                    if curtime > self.cmdtime + self.threshold:
                        self.nortime = curtime
                        return True
                else:
                    self.cmdtime = curtime
            else:
                self.setPos(pos)
                self.nortime = curtime
        return False
