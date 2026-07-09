import sys
from pathlib import Path
from picamera2 import Picamera2
import cv2
sys.path.append(str(Path(__file__).resolve().parent.parent))

from GUI.starterGUIUtilities import initializeGUI
from GUI.starterGUI import StarterGUI
from utilities.cameraUtilities import cleanup, getCameraCaptures, displayImages
from lineFollow.blackLineComputations import getAvgPixelsAndOldPos

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
print(f"Frame Height: {frameHeight}, Frame Width: {frameWidth}")

# Define height and width of the mini monitor
monitorWidth = 800
monitorHeight = 480 

# define size and starting coordinates for named windows
displayWindowWidth = 360
displayWindowHeight = 300
namedWindowStartY = 40

initializeGUI(picam, calibrationGUI, displayWindowWidth, displayWindowHeight, namedWindowStartY, monitorWidth)

# initialize lineFollowState to be go forward
lineFollowState = "fwd"

try:
    while True:
       # get frame from the camera ---> then extract masks for the black line + green squares
       frame, blackLineMask, greenSquareMask, blackPixelCoords, whiteBlobMask = getCameraCaptures(picam)

       # find all average pixels --> break up by top/botom row and left/right col   
       # get old pos, which is the bottom most point
       avgPixels, oldPos = getAvgPixelsAndOldPos(frameWidth, frameHeight, blackLineMask, frame)

       if oldPos == (0,0):
           # in the error gui, display an error for no old pos found
           print("No old pos found")
           continue
       
       imagesToDisplay = [
           (frame, "Frame", (0,namedWindowStartY)), 
           (blackLineMask, "Black Line Mask", (monitorWidth-displayWindowWidth, namedWindowStartY)),
           (whiteBlobMask, "White Blob Mask", (monitorWidth-displayWindowWidth, namedWindowStartY))
        ]
   
       displayImages(imagesToDisplay, displayWindowWidth, displayWindowHeight)
           
       
except KeyboardInterrupt:
    cleanup(picam)
