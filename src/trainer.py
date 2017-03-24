import cv2
import time

class Trainer:
    def __init__(self):
        self.smileCascade = cv2.CascadeClassifier('data/smile.xml')
        self.cmdtime = time.time()
        self.threshold = 5
        
    def predict(self, image, rec):
       if len(rec) == 0:
            return False 
        (x, y, w, h) = rec
        roi_gray = image[y : y + h, x : x + w]
        smile = self.smileCascade.detectMultiScale(roi_gray, 2, 30)
        if len(smile) > 0:
            for (xx, yy, ww, hh) in smile:
                image = cv2.rectangle(roi_gray, (xx, yy), (xx + ww, yy + hh), (0, 255, 255), 2)
            cv2.imshow('smile', image)
            curtime = time.time()
            if curtime - self.cmdtime < self.threshold:
                return False
            else:
                self.cmdtime = curtime
                return True
        else:
            return False

