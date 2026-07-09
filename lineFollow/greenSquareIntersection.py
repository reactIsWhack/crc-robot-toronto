def atGreenSquareIntersection(lineFollowState):
    return lineFollowState == "greenSquareTurnLeft" or lineFollowState == "greenSquareTurnRight" or lineFollowState == "U-Turn"