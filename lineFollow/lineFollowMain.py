from lineFollow.blackLineComputations import getAvgPixelsAndOldPos, getLineCentroid
from lineFollow.greenSquareIntersection import atGreenSquareIntersection
from lineFollow.blackLineComputations import findDestination
import cv2
from utilities.cameraUtilities import getCameraCaptures, displayImages
from utilities.mathUtilities import calcAngleWithHorizontal
from motors.motors import moveFwd, turnRight, turnLeft
from utilities.mathUtilities import checkInRange

pointRadius = 12
destinationPtColor = (255, 182, 193)

def moveToDestination(destinationAngle, lineFollowState):
    errorTo90 = 3
    fwdSpeed = 40
    turnSpeed = 30
    
    # if the destination angle is close to 90, go forward
    if checkInRange(destinationAngle, errorTo90, 90):
        # move robot forward
        moveFwd(fwdSpeed)
        lineFollowState = "fwd"
    elif destinationAngle < 90 or destinationAngle > 270:
        # turn right
        turnRight(turnSpeed)
        lineFollowState = "blackTurnRight"
    else:
        # turn left 
        turnLeft(turnSpeed)
        lineFollowState = "blackTurnLeft"
    return lineFollowState

def moveBasedOnState(lineFollowState, lineCenter, avgPixels, oldPosAngleWithCenter, originalFrame):
    if atGreenSquareIntersection(lineFollowState): 
        # if the state was not updated to be a non green square intersection, we're still in the intersection
        # handle green square intersection
        return
       
    # regular black line --> break up into gap or no gap
    if lineFollowState == "gap":
        pass
    else:
        # straight black line, black line intersection, black line turn
        destinationPt, destinationAngle = findDestination(lineCenter, avgPixels, oldPosAngleWithCenter)

        if destinationPt == (-1, -1):
            # handle no destination pt found 
            return
        
        cv2.circle(originalFrame, destinationPt, pointRadius, destinationPtColor, -1) # draw destination point
        #lineFollowState = moveToDestination(destinationAngle, lineFollowState)

def lineFollow(picam, frameWidth, frameHeight, robotState, namedWindowStartY, monitorWidth, monitorHeight, displayWindowWidth, displayWindowHeight, mainFrameHeight):
    # get frame from the camera ---> then extract masks for the black line + green squares
    frame, blackLineMask, greenSquareMask, blackPixelCoords, whiteBlobMask = getCameraCaptures(picam)
    imagesToDisplay = [
        (frame, "Frame", (10,namedWindowStartY)), # (img, name, left corner position), top left corner
        (whiteBlobMask, "White Blob Mask", (monitorWidth-displayWindowWidth, monitorHeight - displayWindowHeight - 20)), # bottom right corner
        (blackLineMask, "Black Line Mask", (monitorWidth-displayWindowWidth, namedWindowStartY)) # top right corner
    ]

    if len(blackPixelCoords) == 0:
        # handle no black pixels found error here
        displayImages(imagesToDisplay, displayWindowWidth, displayWindowHeight, mainFrameHeight)
        return

    # find all average pixels --> break up by top/botom row and left/right col. avg pixels are candidates for the destination point.
    # get old pos, which is the bottom most point
    avgPixels, oldPos = getAvgPixelsAndOldPos(frameWidth, frameHeight, blackLineMask, frame)

    if oldPos == (0,0):
        # in the error gui, display an error for no old pos found
        print("No old pos found")
        return
    
    if len(avgPixels) == 0 and robotState != "gap":
        # gap encountered
        return
    
    lineCenter = getLineCentroid(blackPixelCoords)
    cv2.circle(frame, lineCenter, pointRadius, (0,255,0), -1)
    # get angle from old pos to center to use as a baseline
    oldPosAngleWithCenter = calcAngleWithHorizontal(oldPos, lineCenter) 

    moveBasedOnState(robotState, lineCenter, avgPixels, oldPosAngleWithCenter, frame)
        

    displayImages(imagesToDisplay, displayWindowWidth, displayWindowHeight, mainFrameHeight)
