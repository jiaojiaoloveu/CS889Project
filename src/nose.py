import cv2
import time
import pyautogui
from helpers import distance

class Nose:

    def __init__(self):
        self.pos = (-1, -1)
        self.rec = (-1, -1, -1, -1)
        self.dis = 0
        self.cmdtime = time.time()
        self.timethreshold = 1
        self.disthreshold = 4 

    def getDis(self):
        return self.dis

    def getPos(self):
        return self.pos

    def setPos(self, rec):
        (x, y, w, h) = rec
        self.pos = (x + w / 2, y + h / 2)
        self.rec = rec

    def update(self, rec):
        cmd = "undefined"
        if len(rec) == 0:
            return cmd
        (x, y, w, h) = rec
        curpointer = (x + w / 2, y + h / 2)
        curtime = time.time()
        if curtime - self.cmdtime > self.timethreshold and not self.pos == (-1, -1):
            self.cmdtime = curtime
            (move, dis) = distance(curpointer, self.pos)
            self.dis = 0.5 * dis
            if max(abs(move[0]), abs(move[1])) > self.disthreshold:
                if abs(move[0]) > abs(move[1]):
                    if move[0] > 0:            
                        cmd = "right"
                    else:
                        cmd = "left"
                else:
                    if move[1] > 0:
                        cmd = 'down'
                    else:
                        cmd = 'up'
        self.setPos(rec)
        return cmd
        
