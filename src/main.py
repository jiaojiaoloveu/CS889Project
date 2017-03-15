import cv2
import numpy as np

camera = cv2.VideoCapture(0)

front_face_detector = cv2.CascadeClassifier('data/frontface.xml')

al_eye_detector = cv2.CascadeClassifier('data/alleyes.xml')

eye_detector = cv2.CascadeClassifier('data/eye.xml')

mouth_detector = cv2.CascadeClassifier('data/mouth.xml')

nose＿detector = cv2.CascadeClassifier('data/nose.xml')

while(True):

    ret, frame = camera.read()

    image = frame.copy()

    image = cv2.flip(image, 1)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    front_face = front_face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in front_face:
        
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)        

        roi_color = image[y : y + h, x : x + w]

        roi_gray = gray[y : y + h, x : x + w]
    
        aleye = al_eye_detector.detectMultiScale(roi_gray)

        for (xx, yy, ww, hh) in aleye:

            roi_eye_color = roi_color[yy : yy + hh, xx : xx + ww]
            roi_eye_gray = roi_gray[yy : yy + hh, xx : xx + ww]

            eyes = eye_detector.detectMultiScale(roi_eye_gray)
        
            if len(eyes) == 2:

                for (ex, ey, ew, eh) in eyes:

                    cv2.rectangle(roi_eye_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        mouth = mouth_detector.detectMultiScale(roi_gray, 2, 20, 0, (30, 30), (500, 500))
        
        for (xx, yy, ww, hh) in mouth:
            
            cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 0, 255), 2)

        nose = nose_detector.detectMultiScale(roi_gray, 1.5, 10, 0, (20, 20))

        for (xx, yy, ww, hh) in nose:

           cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 255), 2)
    
    cv2.imshow('image', image)
    
    key = cv2.waitKey(5)
    
    if key & 0xFF == ord('q'):
        break

camera.release()

cv2.destroyAllWindows()
