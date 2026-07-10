from lineFollow.lineFollowMain import lineFollow
from utilities.cameraUtilities import cleanup, displayPreview
from picamera2 import Picamera2
from GUI.starterGUI import StarterGUI
from GUI.starterGUIUtilities import initializeGUI
from collections import deque

# Initialize picam
# DISCLAIMER: Images from the camera will be in BGR --> RGB means BGR
picam = Picamera2()
config = picam.create_preview_configuration(main={"format":"RGB888", "size":(640,480)})
picam.configure(config)
picam.set_controls({
    "AeEnable": False,
    "ExposureTime": 3000,
    "AnalogueGain": 1
})
picam.start()


# Get height and width of the frame from the cameraa
sampleFrame = picam.capture_array()
frameHeight, frameWidth = sampleFrame.shape[:2]


# Define height and width of the mini monitor
monitorWidth = 800
monitorHeight = 480 

# define size and starting coordinates for named windows
displayWindowWidth = 360
displayWindowHeight = monitorHeight//2 - 50
namedWindowStartY = 40
mainFrameHeight = 400 # main frames include the original frame and the preview 

# initialize robotState to be go forward
robotState = "fwd"

# Create and initialize calibration GUI object
calibrationGUI = StarterGUI()
initializeGUI(picam, calibrationGUI, displayWindowWidth, displayWindowHeight, namedWindowStartY, monitorWidth, mainFrameHeight)

'''
Two threads:

error GUI thread --> will be the main thread to handle updating/showing/hiding the error GUI
robot thread --> all the core line following/evac zone logic is executed on this thread

this way, the program will still be able to execute other logic even with the mainloop() being present
'''

errorQueue = deque()

def runRobot():
    try:
        while True:
            lineFollow(picam, frameWidth, frameHeight, robotState, namedWindowStartY, monitorWidth, monitorHeight, displayWindowWidth, displayWindowHeight, mainFrameHeight)
    except KeyboardInterrupt:
        cleanup(picam)


runRobot()
# robotThread = threading.Thread(target=runRobot, daemon=True)
# robotThread.start()

# errorPopup = ErrorPopup()
# errorPopup.displayWindow()