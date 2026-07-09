import neopixel
import board

num_leds = 8
pixel_pin = board.D18

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_leds,
    brightness=0.5,
    pixel_order=neopixel.RGB
)

def setLed(r, g, b):
    print(r, g, b)
    for i in range(len(pixels)):
        pixels[i] = (r, g, b)

def turnLedRingOn():
    setLed(255, 255, 255)

def turnLedRingOff():
    setLed(0, 0, 0)

# while True:
#     state = input("Enter state for led ring: ")

#     if state == "on":
#         turnLedRingOn()
#     else:
#         turnLedRingOff()