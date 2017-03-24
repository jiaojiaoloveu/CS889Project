import cv2
import math

def distance(pointer, cursor):
    
    move = (pointer[0] - cursor[0], pointer[1] - cursor[1])

    dis = math.sqrt(pow(abs(move[0]), 2) + pow(abs(move[1]), 2))
    
    return (move, dis)


