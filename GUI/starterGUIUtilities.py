import cv2
from lineFollow.ledRing import turnLedRingOff
from time import sleep
from utilities.cameraUtilities import displayPreview

def onClose(calibrationGUI):
    turnLedRingOff()
    calibrationGUI.window.destroy()

def initializeGUI(picam, calibrationGUI, displayWindowWidth, displayWindowHeight, yCoord, monitorWidth, mainFrameHeight):
    calibrationGUI.createButtons() # place buttons on GUI
    calibrationGUI.createRGBLabels() # place rgb labels with default values

    # define the coordinates of the top-left corner of the "Preview" image
    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Preview", displayWindowWidth, mainFrameHeight)
    cv2.moveWindow("Preview", monitorWidth-displayWindowWidth, yCoord)

    sleep(2)
    displayPreview(picam, calibrationGUI)
        
    calibrationGUI.window.protocol("WM_DELETE_WINDOW", lambda: onClose(calibrationGUI))
    calibrationGUI.displayWindow() # start displaying the GUI

