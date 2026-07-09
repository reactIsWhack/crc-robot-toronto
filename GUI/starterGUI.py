from tkinter import *
from lineFollow.ledRing import setLed
import cv2

class StarterGUI:
    def __init__(self, picam):
        self.window = Tk()
        self.picam = picam
        
        # define button size
        self.button_width = 105
        self.button_height = 60

        # define window size
        self.window_width = 400
        self.window_height = 400
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.window.resizable(False, False) # make window unable to be resized

        self.redIncButton = Button(self.window, text="Red Increase")
        self.redDecButton = Button(self.window, text="Red Decrease")
        self.blueIncButton = Button(self.window, text="Blue Increase")
        self.blueDecButton = Button(self.window, text="Blue Decrease")
        self.greenIncButton = Button(self.window, text="Green Increase")
        self.greenDecButton = Button(self.window, text="Green Decrease")
        # coarseButton toggles b/w coarse and fine states
        self.coarseButton = Button(self.window, text="Mode: Coarse")
        self.buttons = [self.redIncButton, self.redDecButton, self.blueIncButton, self.blueDecButton, self.greenIncButton, self.greenDecButton]
        
        self.red = 255
        self.blue = 130
        self.green = 255
        setLed(self.red, self.green, self.blue)
        self.coarse = True
        self.changeAmnt = 25
        self.red_label = Label(self.window, text=f"r: {self.red}",)
        self.green_label = Label(self.window, text=f"g: {self.green}")
        self.blue_label = Label(self.window, text=f"b: {self.blue}")

        self.horizontalPadding = 10
        self.start_y = 15
        self.buttonGridSpacing = 20
        self.gridEndY = 0

        # BIG START BUTTON
        self.startButtonWidth = 325
        self.startButtonHeight = 125
        self.startButton = Button(
            self.window,
            text="START",
            font=("Arial", 24, "bold"),
            bg="green",
            fg="white",
        )
    
    def buttonUpdates(self):
        self.updateRGBLabels()
        setLed(self.red, self.green, self.blue)
        preview = self.picam.capture_array()
        cv2.imshow("Preview", preview)
        cv2.waitKey(1)
    
    # functions for updating values of r, g, b
    def decRed(self):
        self.red = max(0, self.red-self.changeAmnt)
        self.buttonUpdates()
    def incRed(self):
        self.red = min(255, self.red+self.changeAmnt)
        self.buttonUpdates()
    def decBlue(self):
        self.blue = max(0, self.blue-self.changeAmnt)
        self.buttonUpdates()
    def incBlue(self):
        self.blue = min(255, self.blue+self.changeAmnt)
        self.buttonUpdates()
    def decGreen(self):
        self.green = max(0, self.green-self.changeAmnt)
        self.buttonUpdates()
    def incGreen(self):
        self.green = min(255, self.green+self.changeAmnt)
        self.buttonUpdates()
    
    # switch mode b/w coarse and fine
    def switchMode(self):
        self.coarse = False if self.coarse else True
        if self.coarse:
            self.changeAmnt = 25
            self.coarseButton.config(text="Mode: Coarse")
        else:
            self.changeAmnt = 2
            self.coarseButton.config(text="Mode: Fine")
    
    # initialize buttons --> place them on the GUI
    def createButtons(self):

        remainingSpace = self.window_width - 3 * self.button_width - 2 * self.horizontalPadding
        spacing = remainingSpace / 2
        maxY = 0
        for i in range(0,  2):
            yCoord = self.start_y + (self.button_height + self.buttonGridSpacing) * i
            maxY = max(yCoord, maxY)
            for j in range(0, 3):
                idx = j + 3 if i == 1 else j
                button = self.buttons[idx]
                button.place(x=self.horizontalPadding + j*(self.button_width + spacing), y=yCoord, width=self.button_width, height=self.button_height)

        # PLACE BIG START BUTTON
        shiftDown = 50
        self.startButton.place(
            x=self.window_width / 2 - self.startButtonWidth/2,
            y=self.window_height / 2 + shiftDown,
            width=self.startButtonWidth,
            height=self.startButtonHeight
        )
        # place the button for toggling b/w coarse and fine
        verticalSpace = 15
        self.gridEndY = maxY+self.button_height+verticalSpace
        self.coarseButton.place(x=self.horizontalPadding, y=self.gridEndY, width=self.button_width, height=self.button_height)

        # when a button is clicked on, call the appropriate function for inc/dec
        self.redDecButton.config(command=self.decRed)
        self.redIncButton.config(command=self.incRed)
        self.blueDecButton.config(command=self.decBlue)
        self.blueIncButton.config(command=self.incBlue)
        self.greenDecButton.config(command=self.decGreen)
        self.greenIncButton.config(command=self.incGreen)
        self.coarseButton.config(command=self.switchMode)
        self.startButton.config(command=self.closeStarterGUI)
    
    # placing labels "r: red default", "g: green default", "b: blue default" on GUI
    def createRGBLabels(self):
        labelWidth = 70
        horizontalSpaceFromGrid = 30
        verticalSpaceFromGrid = 15
        startX = self.horizontalPadding + self.button_width + horizontalSpaceFromGrid
        spacing = 15
        
        self.red_label.place(x=startX, y=self.gridEndY+verticalSpaceFromGrid, width=labelWidth)
        self.blue_label.place(x=startX+labelWidth+spacing, y=self.gridEndY+verticalSpaceFromGrid, width=labelWidth)
        self.green_label.place(x=startX+2*(labelWidth + spacing), y=self.gridEndY+verticalSpaceFromGrid, width=labelWidth)

    # update the labels for r, g, b with the new values
    def updateRGBLabels(self):
        self.red_label.config(text=f"r: {self.red}")
        self.blue_label.config(text=f"b: {self.blue}")
        self.green_label.config(text=f"g: {self.green}")
    
    # mainloop effectively creates a while true loop
    def displayWindow(self):
        self.window.mainloop() # PROGRAM GETS STUCK HERE --> HAVE TO CLOSE WINDOW TO GET UNSTUCK

    def closeStarterGUI(self):
        self.window.destroy()
        cv2.destroyAllWindows()

    