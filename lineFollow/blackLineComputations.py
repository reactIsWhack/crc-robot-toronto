import cv2
import numpy as np

pointRadius = 12
avgPixelColor = (0, 0, 255)
oldPosColor = (255,0,0)
intervalLenThreshold = 30

def avgPixelOperations(length, avgPixel, avgPixels):
    # if the length of the interval is less than the threshold, don't count the pixel as an average pixel
    if length < intervalLenThreshold:
        return
    
    avgPixels.append(avgPixel)

def findAvgPixelsRows(row, blackLineMask, width):
    # if the first pixel in the row is black, the start is the first pixel in the row = 0
    start = 0 if blackLineMask[row][0] == 0 else -1
    end = -1
    
    avgPixels = [] # each child of intervals is a tuple of the form (length, avgPixel = (x, y))
    for i in range(0, width-1):
        currPixel = blackLineMask[row][i]

        # check for a start pixel
        if currPixel == 0 and blackLineMask[row][i - 1] == 255:
            start = i
            continue

        # check for an end pixel
        if currPixel == 0 and blackLineMask[row][i + 1] == 255:
            end = i

            # calculate avg pixel (middle pixel)
            avgPixelX = (start + end) // 2
            avgPixelOperations(end-start, (avgPixelX, row), avgPixels)
        
            # reset start and end
            start = end = -1
    
    # if the last pixel in the row is black and no end was found before, that means the last pixel in the row is an end
    if end == -1 and blackLineMask[row][width-1] == 0:
        # last pixel in the row = width - 1
        end = width - 1
        avgPixelOperations(end-start, ((start+end)//2, row), avgPixels)
    return avgPixels

def findAvgPixelsCols(col, blackLineMask, height):
    # if the first pixel in the col is black, the start is the first pixel in the col = 0
    start = 0 if blackLineMask[0][col] == 0 else -1
    end = -1
    
    avgPixels = []
    for i in range(0, height-1):
        currPixel = blackLineMask[i][col]

        # check for a start pixel
        if currPixel == 0 and blackLineMask[i-1][col] == 255:
            start = i
            continue

        # check for an end pixel
        if currPixel == 0 and blackLineMask[i+1][col] == 255:
            end = i

            # calculate avg pixel (middle pixel)
            avgPixelY = (start + end) // 2
            avgPixelOperations(end-start, (col, avgPixelY), avgPixels)
        
            # reset start and end
            start = end = -1
    
    # if the last pixel in the col is black and no end was found before, that means the last pixel in the column is an end
    if end == -1 and blackLineMask[height-1][col] == 0:
        # last pixel in column = height - 1
        end = height - 1
        avgPixelOperations(end-start, (col, (end+start)//2), avgPixels)
    return avgPixels

def getAvgPixelsAndOldPos(width, height, blackLineMask, originalFrame):
    topAvgPixels = findAvgPixelsRows(0, blackLineMask, width)
    bottomAvgPixels = findAvgPixelsRows(height-1, blackLineMask, width)
    leftAvgPixels = findAvgPixelsCols(0, blackLineMask, height)
    rightAvgPixels = findAvgPixelsCols(width-1, blackLineMask, height)

    avgPixels = []
    avgPixels.extend(topAvgPixels)
    avgPixels.extend(bottomAvgPixels)
    avgPixels.extend(leftAvgPixels)
    avgPixels.extend(rightAvgPixels)

    # find the old pos using the avgPixels --> old pos is the bottom most point (the point with the largest Y)
    # also remove old pos from averagePixels
    oldPos = findOldPos(avgPixels)

    # display avg pixels
    for avgPixel in avgPixels:
        cv2.circle(originalFrame, avgPixel, pointRadius, avgPixelColor, -1)

    cv2.circle(originalFrame, oldPos, pointRadius, oldPosColor, -1) # display the old pos point

    return avgPixels, oldPos 

def findOldPos(avgPixels):
    oldPos = (0, 0)
    idx = -1

    # find point with the largest Y coordinate --> this is old pos
    for i, avgPixel in enumerate(avgPixels):
        if avgPixel[1] > oldPos[1]:
            oldPos = avgPixel
            idx = i

    if idx != -1:
        # remove old pos from avg pixels
        avgPixels.pop(idx)
    
    return oldPos

def getLineCentroid(blackPixelCoords):    
    xSum = 0
    ySum = 0

    for blackPixelCoord in blackPixelCoords:
        # [y, x]
        xSum += blackPixelCoord[1]
        ySum += blackPixelCoord[0]

    if len(blackPixelCoords) == 0:
        return "No Black Pixels Found"

    xCentroid = xSum / len(blackPixelCoords)
    yCentroid = ySum / len(blackPixelCoords)
    return (xCentroid, yCentroid)
