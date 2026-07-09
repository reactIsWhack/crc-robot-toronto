import cv2
from lineFollow.ledRing import turnLedRingOn, turnLedRingOff
from time import sleep

def onClose(calibrationGUI):
    turnLedRingOff()
    calibrationGUI.window.destroy()

def initializeGUI(picam, calibrationGUI, displayWindowWidth, displayWindowHeight, yCoord, monitorWidth):
    calibrationGUI.createButtons() # place buttons on GUI
    calibrationGUI.createRGBLabels() # place rgb labels with default values

    # define the coordinates of the top-left corner of the "Preview" image
    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Preview", displayWindowWidth, displayWindowHeight)
    cv2.moveWindow("Preview", monitorWidth-displayWindowWidth, yCoord)

    sleep(2)

    # display the "Preview" image
    preview = picam.capture_array()
    cv2.imshow("Preview", preview)
    cv2.waitKey(1)
        
    calibrationGUI.window.protocol("WM_DELETE_WINDOW", lambda: onClose(calibrationGUI))
    calibrationGUI.displayWindow() # start displaying the GUI

