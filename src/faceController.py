import cv2
import numpy as np
import time
import math
import pyautogui
from faceDetector import faceDetector

def main():
    color = {'face': (255,  0, 0), 'aleye': (255, 255, 255), 'leye': (0, 255, 255), 'reye': (255, 255, 0), 'nose': (0, 255, 0), 'mouth': (0, 0, 255)}
    camera = cv2.VideoCapture(0)
    while(True):
        ret, frame = camera.read()
        image = frame.copy()
        image = cv2.flip(image, 1)
        detector = faceDetector()
        face = detector.detect(image)
        for key in face:
            (x, y, w, h) = face[key]
            image = cv2.rectangle(image, (x, y), (x + w, y + h), color[key], 2)
        cv2.imshow('image', image)
        key = cv2.waitKey(5)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('p'):
            print(face)
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
