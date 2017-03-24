import cv2
import numpy as np
import sklearn as sk
import time
import math
import pyautogui
from faceDetector import faceDetector
from eye import Eye
from nose import Nose
from mouth import Mouth
from trainer import Trainer
from helpers import *

def getCmd(face, leye, reye, nose, mouth):
    cmd = -1
    pos = nose.getPos()
    lBlink = leye.update(face['aleye'], face['leye'])
    rBlink = reye.update(face['aleye'], face['reye'])
    noseCmd = nose.update(face['nose'])
    mouthCmd = mouth.update(face['mouth'])
    
    if lBlink and rBlink:
        print('double eye closed')
        localtime = time.localtime()
        filename = 'pic/' + str(localtime.tm_year) + str(localtime.tm_mon) + str(localtime.tm_mday) + str(localtime.tm_hour) + str(localtime.tm_min) + str(localtime.tm_sec) + '.jpg'
        pyautogui.screenshot(filename)
    elif lBlink:
        print('left eye')
    elif rBlink:
        print('right eye')

    if noseCmd == 'up':
        print('nose up')
        pyautogui.scroll(nose.getDis())
    elif noseCmd == 'down':
        print('nose down')
        pyautogui.scroll(-nose.getDis())
    elif noseCmd == 'left':
        print('nose left')
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.keyUp('alt')
    elif noseCmd == 'right':
        print('nose right')
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.press('left')
        pyautogui.keyUp('alt')

def getShortcut(trainer, image, face):
    smile = trainer.predict(image, face['face'])
    if smile:
        pyautogui.keyDown('alt')
        pyautogui.press('w')
        pyautogui.keyUp('alt')

def main():
    color = {'face': (255,  0, 0), 'aleye': (255, 255, 255), 'leye': (0, 255, 255), 'reye': (255, 255, 0), 'nose': (0, 255, 0), 'mouth': (0, 0, 255)}
    camera = cv2.VideoCapture(0)
    detector = faceDetector()
    leye = Eye()
    reye = Eye()
    nose = Nose()
    mouth = Mouth()    
    trainer = Trainer()
    while(True):
        ret, frame = camera.read()
        image = frame.copy()
        image = cv2.flip(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face = detector.detect(gray)
        getShortcut(trainer, gray, face)
        for key in face:
            if len(face[key]) == 0:
                continue
            (x, y, w, h) = face[key]
            image = cv2.rectangle(image, (x, y), (x + w, y + h), color[key], 2)
        cv2.imshow('image', image)
        #getCmd(face, leye, reye, nose, mouth)

        key = cv2.waitKey(5)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('p'):
            print(face)
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
