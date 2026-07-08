from lineFollow.ledRing import turnLedRingOff
import cv2
import numpy as np

# define lower and upper bounds for masks, in hsv
blackLineLower = np.array([0, 0, 0])
blackLineUpper = np.array([180, 255, 50])
lowerGreen = np.array([35, 60, 60])
upperGreen = np.array([85, 255, 255])

def cleanup(picam):
    picam.stop()
    turnLedRingOff()

def getCameraCaptures(picam):
    frame = picam.capture_array()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # copy of frame in hsv for masks
    '''
    Create two masks:

    1st --> Isolates green squares as white regions
    2nd --> Isolates black line as white, white regions become black. 
            Invert to get the line to be black.
    '''

    blackLineMask = cv2.inRange(frameHSV, blackLineLower, blackLineUpper)
    blackLineMask = cv2.bitwise_not(blackLineMask) # invert black line mask
    greenSquareMask = cv2.inRange(frameHSV, lowerGreen, upperGreen)    

    return frame, blackLineMask, greenSquareMask 

def handleNoOldPosFound():
    pass