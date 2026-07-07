import math

def calcAngleWithHorizontal(originPt, finalPt):
    originX, originY = originPt
    finalX, finalY = finalPt

    angle = math.degrees(math.atan2(-finalY + originY, finalX - originX))
    if finalY > originY:
        angle += 360
        
    return angle