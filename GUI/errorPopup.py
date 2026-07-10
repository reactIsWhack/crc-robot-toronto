from tkinter import *

class ErrorPopup:
    def __init__(self):
        self.window = Tk()
        
        # define window size
        self.windowWidth = 500
        self.windowHeight = 400
        self.window.geometry(f"{self.windowWidth}x{self.windowHeight}")
        self.window.resizable(False, False) # make window unable to be resized
        
        # define and position the static "ERROR" header
        self.errorHeaderWidth = 100
        self.errorHeaderYCoord = 10
        self.errorHeader = Label(self.window, text="Errors", font=("Arial", 24, "bold"), fg="#B61F04")  # Font family, size, style)
        self.errorHeader.place(x=(self.windowWidth / 2) - (self.errorHeaderWidth / 2), y=self.errorHeaderYCoord, width=self.errorHeaderWidth)
                
    def displayWindow(self):
        self.window.mainloop()