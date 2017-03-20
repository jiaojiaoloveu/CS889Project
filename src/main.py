import cv2
import numpy as np

camera = cv2.VideoCapture(0)

front_face_detector = cv2.CascadeClassifier('data/frontface.xml')

al_eye_detector = cv2.CascadeClassifier('data/alleyes.xml')

eye_detector = cv2.CascadeClassifier('data/eye.xml')

mouth_detector = cv2.CascadeClassifier('data/mouth.xml')

nose＿detector = cv2.CascadeClassifier('data/nose.xml')

def faceDetector(image):

    face = {}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    front_face = front_face_detector.detectMultiScale(gray, 1.3, 5)

    if len(front_face) == 1:

        (x, y, w, h) = front_face[0]

        face['face'] = (x, y, w, h)
        
        roi_color = image[y : y + h, x : x + w]

        roi_gray = gray[y : y + h, x : x + w]
    
        aleye = al_eye_detector.detectMultiScale(roi_gray)

        if len(aleye) == 1:

            (xx, yy, ww, hh) = aleye[0]

            face['aleye'] = (xx + x, yy + y, ww, hh)

            roi_eye_color = roi_color[yy : yy + hh, xx : xx + ww]

            roi_eye_gray = roi_gray[yy : yy + hh, xx : xx + ww]

            eyes = eye_detector.detectMultiScale(roi_eye_gray)

            if len(eyes) == 2:
            
                face['leye'] = eyes[0] + (xx, yy, 0, 0) + (x, y, 0, 0)

                face['reye'] = eyes[1] + (xx, yy, 0, 0) + (x, y, 0, 0)

                if face['leye'][0] > face['reye'][0]:
                    
                    tmpeye = face['leye']
                    
                    face['leye'] = face['reye']
                    
                    face['reye'] = tmpeye
            
            elif len(eyes) == 1:
                
                (ex, ey, ew, eh) = eyes[0]
            
                if ex > ww / 2:
                    
                    face['reye'] = (ex + xx + x, ey + yy + y, ew, eh)

                else:

                    face['leye'] = (ex + xx + x, ey + yy + y, ew, eh)

                    
        mouth = mouth_detector.detectMultiScale(roi_gray, 1.8, 20, 0, (30, 30), (500, 500))
        
        if len(mouth) == 1:
       
            (xx, yy, ww, hh) = mouth[0]
        
            face['mouth'] = (x + xx, y + yy, ww, hh)
        
        nose = nose_detector.detectMultiScale(roi_gray, 1.3, 8)

        if len(nose) == 1:
        
           (xx, yy, ww, hh) = nose[0]
    
           face['nose'] = (x + xx, y + yy, ww, hh)

    return face 

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
 
    
camera.release()

cv2.destroyAllWindows()
