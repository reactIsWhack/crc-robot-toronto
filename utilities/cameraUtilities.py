from lineFollow.ledRing import turnLedRingOff
import cv2
import numpy as np

# define lower and upper bounds for masks, in hsv
blackLineLower = np.array([0, 0, 0])
blackLineUpper = np.array([180, 255, 50])
lowerGreen = np.array([35, 60, 60])
upperGreen = np.array([85, 255, 255])
whiteBlobLower = np.array([0, 0, 90])
whiteBlobUpper = np.array([180, 40, 255])

def cleanup(picam):
    picam.stop()
    turnLedRingOff()

def getCameraCaptures(picam):
    frame = picam.capture_array()
    frame = cv2.GaussianBlur(frame, (5,5), 0) # blur the frame
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
    whiteBlobMask = cv2.inRange(frameHSV, whiteBlobLower, whiteBlobUpper)

    # apply tophat morpholgoical transformation to fill in white spots left by led ring
    kernel = np.ones((8,8), np.uint8)
    whiteBlobMask = cv2.erode(whiteBlobMask, kernel, iterations=30)
    whiteBlobMask = cv2.GaussianBlur(whiteBlobMask, (5,5), 0)

    # return coordinates of elements (pixels) == 0 in blackLineMask --> return coordinates of black pixels
    blackPixelCoords = np.argwhere(blackLineMask == 0)
 
    return frame, blackLineMask, greenSquareMask, blackPixelCoords, whiteBlobMask

def displayImages(images, displayWindowWidth, displayWindowHeight):
    '''
    images = [(image, name, position)]
    position = (x, y)
    '''

    for item in images:
        image, name, position = item

        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, displayWindowWidth, displayWindowHeight)
        cv2.moveWindow(name, position[0], position[1])
        cv2.imshow(name, image)

    cv2.waitKey(1)