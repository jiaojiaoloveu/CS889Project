import cv2
import numpy

camera = cv2.VideoCapture(0)

while(True):

    ret, frame = camera.read()

    image = frame.copy()

    image = cv2.flip(image, 1)
    
    cv2.imshow('image', image)
    
    key = cv2.waitKey(5)
    
    if key & 0xFF == ord('q'):
        break

camera.release()

cv2.destroyAllWindows()
