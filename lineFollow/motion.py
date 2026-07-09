from lineFollow.greenSquareIntersection import atGreenSquareIntersection
from lineFollow.blackLineComputations import findDestination
import cv2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utilities.mathUtilities import checkInRange
from motors.motors import moveFwd, turnRight, turnLeft

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
        


def lineFollow(lineFollowState, lineCenter, avgPixels, oldPosAngleWithCenter, originalFrame):
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
