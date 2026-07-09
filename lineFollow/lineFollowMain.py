import sys
from pathlib import Path
from blackLineComputations import getAvgPixelsAndOldPos, getLineCentroid
from motion import moveBasedOnState
from lineFollow.greenSquareIntersection import atGreenSquareIntersection
from lineFollow.blackLineComputations import findDestination
import cv2
sys.path.append(str(Path(__file__).resolve().parent.parent))

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
        cv2.circle(originalFrame, destinationPt, pointRadius, destinationPtColor, -1) # draw destination point
        #lineFollowState = moveToDestination(destinationAngle, lineFollowState)

def lineFollow(picam, frameWidth, frameHeight, robotState, namedWindowStartY, monitorWidth, displayWindowWidth, displayWindowHeight):
    # get frame from the camera ---> then extract masks for the black line + green squares
    frame, blackLineMask, greenSquareMask, blackPixelCoords, whiteBlobMask = getCameraCaptures(picam)

    if len(blackPixelCoords) == 0:
        # handle no black pixels found error here
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
    # get angle from old pos to center to use as a baseline
    oldPosAngleWithCenter = calcAngleWithHorizontal(oldPos, lineCenter) 

    moveBasedOnState(robotState, lineCenter, avgPixels, oldPosAngleWithCenter)
        
    imagesToDisplay = [
        (frame, "Frame", (0,namedWindowStartY)), # (img, name, left corner position)
        (blackLineMask, "Black Line Mask", (monitorWidth-displayWindowWidth, namedWindowStartY)),
        (whiteBlobMask, "White Blob Mask", (monitorWidth-displayWindowWidth, namedWindowStartY))
    ]

    displayImages(imagesToDisplay, displayWindowWidth, displayWindowHeight)
