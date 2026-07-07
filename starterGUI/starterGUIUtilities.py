from starterGUI.starterGUI import StarterGUI
import cv2

monitorWidth = 800
calibrationGUI = StarterGUI()

def initializeGUI(frameWidth, picam):
    calibrationGUI.createButtons() # place buttons on GUI
    calibrationGUI.createRGBLabels() # place rgb labels with default values

    # define the coordinates of the top-left corner of the "Preview" image
    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Preview", monitorWidth-frameWidth+200, 0)

    # display the "Preview" image
    preview = picam.capture_array()
    cv2.imshow("Preview", preview)
        
    calibrationGUI.displayWindow() # start displaying the GUI
    '''
    while True:
        ~~~~~~~~
    '''