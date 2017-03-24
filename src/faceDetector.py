import cv2

class faceDetector:

    def __init__(self):
        self.front_face_detector = cv2.CascadeClassifier('data/frontface.xml')
        self.al_eye_detector = cv2.CascadeClassifier('data/alleyes.xml')
        self.eye_detector = cv2.CascadeClassifier('data/eye.xml')
        self.mouth_detector = cv2.CascadeClassifier('data/mouth.xml')
        self.nose＿detector = cv2.CascadeClassifier('data/nose.xml')

    def detect(self, gray):
        face = {'face': (), 'aleye': (), 'leye': (), 'reye': (), 'mouth': (), 'nose': ()}
#        cv2.imshow('gray', gray)
        front_face = self.front_face_detector.detectMultiScale(gray, 1.3, 5)
        if len(front_face) == 1:
            (x, y, w, h) = front_face[0]
            face['face'] = (x, y, w, h)
            roi_gray = gray[y : y + h, x : x + w]
            aleye = self.al_eye_detector.detectMultiScale(roi_gray)
            if len(aleye) == 1:
                (xx, yy, ww, hh) = aleye[0]
                face['aleye'] = (xx + x, yy + y, ww, hh)
                roi_eye_gray = roi_gray[yy : yy + hh, xx : xx + ww]
                eyes = self.eye_detector.detectMultiScale(roi_eye_gray)
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
            mouth = self.mouth_detector.detectMultiScale(roi_gray, 1.8, 20, 0, (30, 30), (500, 500))
            if len(mouth) == 1:
                (xx, yy, ww, hh) = mouth[0]
                face['mouth'] = (x + xx, y + yy, ww, hh)
            nose = self.nose_detector.detectMultiScale(roi_gray, 1.3, 8)
            if len(nose) == 1:
                (xx, yy, ww, hh) = nose[0]
                face['nose'] = (x + xx, y + yy, ww, hh)
        return face   
