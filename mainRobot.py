from lineFollow.lineFollowMain import lineFollow
from utilities.cameraUtilities import cleanup
from picamera2 import Picamera2
from GUI.starterGUI import StarterGUI
from GUI.starterGUIUtilities import initializeGUI
from GUI.errorPopup import ErrorPopup
import threading
from collections import deque

# Initialize picam
# DISCLAIMER: Images from the camera will be in BGR --> RGB means BGR
picam = Picamera2()
config = picam.create_preview_configuration(main={"format":"RGB888", "size":(640,480)})
picam.configure(config)
picam.start()

# Create calibration GUI and error popup GUI objects
calibrationGUI = StarterGUI(picam)

# Get height and width of the frame from the cameraa
sampleFrame = picam.capture_array()
frameHeight, frameWidth = sampleFrame.shape[:2]

# define size and starting coordinates for named windows
displayWindowWidth = 360
displayWindowHeight = 300
namedWindowStartY = 40

# Define height and width of the mini monitor
monitorWidth = 800
monitorHeight = 480 

# initialize robotState to be go forward
robotState = "fwd"

initializeGUI(picam, calibrationGUI, displayWindowWidth, displayWindowHeight, namedWindowStartY, monitorWidth)

'''
Two threads:

error GUI thread --> will be the main thread to handle updating/showing/hiding the error GUI
robot thread --> all the core line following/evac zone logic is executed on this thread

this way, the program will still be able to execute other logic even with the mainloop() being present
'''

errorQueue = deque()

def runRobot():
    while True:
        lineFollow(picam, frameWidth, frameHeight, robotState, namedWindowStartY, monitorWidth, displayWindowWidth, displayWindowHeight)



robotThread = threading.Thread(target=runRobot, daemon=True)
robotThread.start()

errorPopup = ErrorPopup()
errorPopup.displayWindow()