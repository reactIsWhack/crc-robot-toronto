from gpiozero import OutputDevice, PWMOutputDevice

# define pin numbers
backRightENAPin = 22
backRightIN1Pin = 27
backRightIN2Pin = 17
backLeftIN3Pin = 14
backLeftIN4Pin = 15
backLeftENBPin = 23

frontRightENAPin = 21
frontRightIN1Pin = 20
frontRightIN2Pin = 16
frontLeftIN3Pin = 26
frontLeftIN4Pin = 19
frontLeftENBPin = 13

# set up GPIO pins for in pins
backRightIN1 = OutputDevice(backRightIN1Pin)
backRightIN2 = OutputDevice(backRightIN2Pin)
backLeftIN3 = OutputDevice(backLeftIN3Pin)
backLeftIN4 = OutputDevice(backLeftIN4Pin)

frontRightIN1 = OutputDevice(frontRightIN1Pin)
frontRightIN2 = OutputDevice(frontRightIN2Pin)
frontLeftIN3 = OutputDevice(frontLeftIN3Pin)
frontLeftIN4 = OutputDevice(frontLeftIN4Pin)

backRightENA = PWMOutputDevice(backRightENAPin)
backLeftENB = PWMOutputDevice(backLeftENBPin)
frontRightENA = PWMOutputDevice(frontRightENAPin)
frontLeftENB = PWMOutputDevice(frontLeftENBPin)

def moveFL(speed, direction):
    reverse = True
    if reverse:
        direction = "fwd" if direction == "bwd" else "bwd"
    
    if direction == "fwd":
        frontLeftIN3.on()
        frontLeftIN4.off()
    elif direction == "bwd":
        frontLeftIN3.off()
        frontLeftIN4.on()
    frontLeftENB.value = speed/100

def moveFR(speed, direction):
    reverse = True
    if reverse:
        direction = "fwd" if direction == "bwd" else "bwd"
    
    if direction == "fwd":
        frontRightIN1.on()
        frontRightIN2.off()
    elif direction == "bwd":
        frontRightIN1.off()
        frontRightIN2.on()
    frontRightENA.value = speed/100

def moveBL(speed, direction):
    reverse = True
    if reverse:
        direction = "fwd" if direction == "bwd" else "bwd"
    
    if direction == "fwd":
        backLeftIN3.on()
        backLeftIN4.off()
    elif direction == "bwd":
        backLeftIN3.off()
        backLeftIN4.on()
    backLeftENB.value = speed/100

def moveBR(speed, direction):
    reverse = False
    if reverse:
        direction = "fwd" if direction == "bwd" else "bwd"
    
    if direction == "fwd":
        backRightIN1.on()
        backRightIN2.off()
    elif direction == "bwd":
        backRightIN1.off()
        backRightIN2.on()
    backRightENA.value = speed/100

def moveFwd(speed):
    moveFL(speed, "fwd")
    moveFR(speed, "fwd")
    moveBL(speed, "fwd")
    moveBR(speed, "fwd")

def moveBwd(speed):
    moveFL(speed, "bwd")
    moveFR(speed, "bwd")
    moveBL(speed, "bwd")
    moveBR(speed, "bwd")

def turnLeft(speed):
    # right fwd, left bwd
    moveFL(speed, "bwd")
    moveFR(speed, "fwd")
    moveBL(speed, "bwd")
    moveBR(speed, "fwd")

def turnRight(speed):
    # right bwd, left fwd
    moveFL(speed, "fwd")
    moveFR(speed, "bwd")
    moveBL(speed, "fwd")
    moveBR(speed, "bwd")

def stopRobot():
    frontLeftENB.value = 0
    frontRightENA.value = 0
    backLeftENB.value = 0
    backRightENA.value = 0