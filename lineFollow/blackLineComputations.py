import cv2
import numpy as np

pointRadius = 6
avgPixelColor = (0, 0, 255)

def avgPixelOperations(xCoord, yCoord, avgPixels, originalFrame):
    avgPixel = (xCoord, yCoord)
    avgPixels.append(avgPixel)

    # display the average pixel on the original frame
    cv2.circle(originalFrame, avgPixel, pointRadius, avgPixelColor, -1)

def findAvgPixelsRows(row, blackLineMask, width, originalFrame):
    # if the first pixel in the row is black, the start is the first pixel in the row = 0
    start = 0 if blackLineMask[row][0] == 0 else -1
    end = -1
    
    avgPixels = []
    for i in range(0, width):
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
            avgPixelOperations(avgPixelX, row, avgPixels, originalFrame)
        
            # reset start and end
            start = end = -1
    
    # if we get to the end of the row and no end was the found, that means the last pixel in the row is an end
    if end == -1:
        # last pixel in the row = width - 1
        end = width - 1
        avgPixelOperations((start+end)//2, row, avgPixels, originalFrame)
    return avgPixels

def findAvgPixelsCols(col, blackLineMask, height, originalFrame):
    # if the first pixel in the col is black, the start is the first pixel in the col = 0
    start = 0 if blackLineMask[col][0] == 0 else -1
    end = -1
    
    avgPixels = []
    for i in range(0, height):
        currPixel = blackLineMask[col][i]

        # check for a start pixel
        if currPixel == 0 and blackLineMask[col][i - 1] == 255:
            start = i
            continue

        # check for an end pixel
        if currPixel == 0 and blackLineMask[col][i + 1] == 255:
            end = i

            # calculate avg pixel (middle pixel)
            avgPixelY = (start + end) // 2
            avgPixelOperations(col, avgPixelY, avgPixels, originalFrame)
        
            # reset start and end
            start = end = -1
    
    # if we get to the end of the column and no end was the found, that means the last pixel in the column is an end
    if end == -1:
        # last pixel in column = height - 1
        end = height - 1
        avgPixelOperations((col, (start + end) // 2, avgPixels, originalFrame))
    return avgPixels

def getAvgPixelsAndOldPos(width, height, blackLineMask, originalFrame):
    topAvgPixels = findAvgPixelsRows(0, blackLineMask, width, originalFrame)
    bottomAvgPixels = findAvgPixelsRows(height-1, blackLineMask, width, originalFrame)
    leftAvgPixels = findAvgPixelsCols(0, blackLineMask, height, originalFrame)
    rightAvgPixels = findAvgPixelsCols(width-1, blackLineMask, height, originalFrame)

    avgPixels = []
    avgPixels.extend(topAvgPixels)
    avgPixels.extend(bottomAvgPixels)
    avgPixels.extend(leftAvgPixels)
    avgPixels.extend(rightAvgPixels)

    # find the old pos using the avgPixels --> old pos is the bottom most point (the point with the largest Y)
    # also remove old pos from averagePixels
    oldPos = findOldPos(avgPixels)

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

def getLineCentroid(blackLineMask, width, height):
    # return coordinates of elements (pixels) == 0 in blackLineMask --> return coordinates of black pixels
    blackPixelCoords = np.argwhere(blackLineMask == 0)
    
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
