import cv2
from picamera2 import Picamera2
from starterGUI.starterGUIUtilities import initializeGUI
from starterGUI.starterGUI import StarterGUI
from time import sleep

# Initialize picam
# DISCLAIMER: Images from the camera will be in BGR --> RGB means BGR
picam = Picamera2()
config = picam.create_preview_configuration(main={"format":"RGB888", "size":(640,480)})
picam.configure(config)
picam.start()

# Create calibrationGUI object
calibrationGUI = StarterGUI(picam)

sampleFrame = picam.capture_array()
frameHeight, frameWidth = sampleFrame.shape[:2]

initializeGUI(frameWidth, picam, calibrationGUI)

picam.stop()