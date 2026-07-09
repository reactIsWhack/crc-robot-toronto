import keyboard
from motors import moveFwd, moveBwd, turnLeft, turnRight, stopRobot

baseSpeed = 50

try:
    while True:
        w_pressed = keyboard.is_pressed('w')
        s_pressed = keyboard.is_pressed('s')
        a_pressed = keyboard.is_pressed('a')
        d_pressed = keyboard.is_pressed('d')

        if not w_pressed and not s_pressed and not a_pressed and not d_pressed:
            stopRobot()
            continue

        if w_pressed:
            moveFwd(baseSpeed)
        elif s_pressed:
            moveBwd(baseSpeed)
        elif a_pressed:
            turnLeft(baseSpeed)
        elif d_pressed:
            turnRight(baseSpeed)

except KeyboardInterrupt:
    print("Program Ended")