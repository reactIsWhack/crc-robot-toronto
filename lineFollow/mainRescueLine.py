from picamera2 import Picamera2
from GUI.starterGUIUtilities import initializeGUI
from GUI.starterGUI import StarterGUI
from utilities.cameraUtilities import cleanup, getCameraCaptures
from lineFollow.blackLineComputations import getAvgPixelsAndOldPos

# Initialize picam
# DISCLAIMER: Images from the camera will be in BGR --> RGB means BGR
picam = Picamera2()
config = picam.create_preview_configuration(main={"format":"RGB888", "size":(640,480)})
picam.configure(config)
picam.start()

# Create calibrationGUI object
calibrationGUI = StarterGUI(picam)

# Get height and width of the frame from the cameraa
sampleFrame = picam.capture_array()
frameHeight, frameWidth = sampleFrame.shape[:2]

initializeGUI(frameWidth, picam, calibrationGUI)

# initialize lineFollowState to be go forward
lineFollowState = "fwd"

try:
    while True:
       # get frame from the camera ---> then extract masks for the black line + green squares
       frame, blackLineMask, greenSquareMask = getCameraCaptures(picam)
       
       # find all average pixels --> break up by top/botom row and left/right col   
       # get old pos, which is the bottom most point
       avgPixels, oldPos = getAvgPixelsAndOldPos(frameWidth, frameHeight, blackLineMask, frame)

       if oldPos == (0, 0):
           # no old found, display the error on the error popup

           continue
           
       
except KeyboardInterrupt:
    cleanup()
