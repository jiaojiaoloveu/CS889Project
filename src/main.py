import cv2
import numpy as np
import pyautogui
import time
import math
from face_detector import faceDetector

pyautogui.FALSESAFE = False

camera = cv2.VideoCapture(0)

debug = True

# seconds
threshold = 0.3

eyetime = -2

leyetime = -2

reyetime = -2

cursor = (-1, -1)

dis_delta = 5

move_alpha = 3

face_alpha = 1.2

head_size = -1

head_flag = False

mouth_time = -1

mouth_alpha = 1.1

keyboard_flag = False

# null: -1
# left eye wink: 0
# right eye wink: 1
# both eye wink: 2
# head move up: 3
# head move down: 4
# head move left: 5
# head move right: 6
# mouth open: 7
# smile: 8

def distance(pointer, cursor):
    
    move = (pointer[0] - cursor[0], pointer[1] - cursor[1])

    dis = math.sqrt(pow(abs(move[0]), 2) + pow(abs(move[1]), 2))
    
    return (move, dis)

def getCMD(face):
    
    now = time.time()

    global eyetime, leyetime, reyetime

    res = {'code': [], 'pos': pyautogui.position()}

    if 'face' in face:
        
        (x, y, w, h) = face['face']
    
        face_area = w * h

        global head_size, head_flag

        print('face size', face_area)

        print('head_size', head_size)

        print(head_flag)

        if head_size > 0 and face_area > face_alpha * head_size:

            head_flag = not head_flag

        head_size = face_area
        
    global mouth_time, mouth_alpha
    
    if 'mouth' not in face:
        
        current = time.time()

        if mouth_time > 0 and current - mouth_time > mouth_alpha:
            res['code'].append(7)
    
        elif mouth_time < 0:
    
            mouth_time = current

    else:


        mouth_time = -1
    
    if 'aleye' in face:
        
        if 'leye' not in face and 'reye' not in face:
            
            if eyetime == -2:
                eyetime = now

            elif eyetime > 0 and now - eyetime > threshold:
                res['code'].append(2)
                eyetime = -1
    
        elif 'leye' not in face:

            if leyetime == -2:
                leyetime = now
            
            elif leyetime > 0 and now - leyetime > threshold:
                res['code'].append(0)
                leyetime = -1

        elif 'reye' not in face:
    
            if reyetime == -2:
                reyetime = now

            elif reyetime > 0 and now - reyetime > threshold:
                res['code'].append(1)
                reyetime = -1

        else:
            
            eyetime = -2
            leyetime = -2
            reyetime = -2
    
    if 'nose' in face:
        
        (xx, yy, ww, hh) = face['nose']
    
        pointer = (xx + ww / 2, yy + hh / 2)
   
        global cursor

        if cursor == (-1, -1):
        
            cursor = pointer
            
        else:
             
            (move, dis) = distance(pointer, cursor)   

            if abs(move[0]) > abs(move[1]):
                if move[0] > 0:
                    res['code'].append(6)
                else:
                    res['code'].append(5)
            else:
                if move[1] > 0:
                    res['code'].append(4)
                else:
                    res['code'].append(3)

            if dis > dis_delta:

                cursor = pointer

                newpos = (res['pos'][0] + move_alpha * move[0], res['pos'][1] + move_alpha * move[1])
            
                res['pos'] = newpos

    return res

def callCMD(image, face):

    res = getCMD(face)
    code = res['code']
    pos = res['pos']

    if debug and len(code) > 0:
        print(code)
        print(pos)

    global keyboard_flag 

    if code == [0]:
        pyautogui.click(pos[0], pos[1])
    elif code == [1]:
        pyautogui.rightClick(pos[0], pos[1])
    elif code == [2]:
        pyautogui.doubleClick(pos[0], pos[1])
    elif code == [3]:
        pyautogui.scroll(5)
    elif code == [4]:
        pyautogui.scroll(-5)
    elif code == [7] and not keyboard_flag:
        print('mouth open')

    pyautogui.moveTo(pos[0], pos[1])

    global head_flag


while(True):

    ret, frame = camera.read()

    image = frame.copy()

    image = cv2.flip(image, 1)
    
    face = faceDetector(image)
       
    color = {'face': (255,  0, 0), 'aleye': (255, 255, 255), 'leye': (0, 255, 255), 'reye': (255, 255, 0), 'nose': (0, 255, 0), 'mouth': (0, 0, 255)}

    for key in face:

        (x, y, w, h) = face[key]

        image = cv2.rectangle(image, (x, y), (x + w, y + h), color[key], 2)

    cv2.imshow('image', image)


    key = cv2.waitKey(5)
    
    if key & 0xFF == ord('q'):

        break

    elif key & 0xFF == ord('p'):
        
        print(face) 
    
    elif key & 0xFF == ord('d'):
        
        debug = ~debug

    callCMD(image, face)

camera.release()

cv2.destroyAllWindows()
