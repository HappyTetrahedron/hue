#!/usr/bin/env python3

import evdev
import hue
from multiprocessing import Process

def listen(device):
    print("process started")
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print(event)
            if (event.value == 1):
                if (event.code == 103):
                    print("up button")
                    hue.scene('focus')
                if (event.code == 108):
                    print("down button")
                    hue.scene('night')
                if (event.code == 106):
                    print("right button")
                    hue.scene('relax')
                if (event.code == 105):
                    print("left button")
                    hue.scene('random')
                if (event.code == 28):
                    print("ok button")
                    hue.scene('last')
                if (event.code == 66):
                    print ("power button")
                    hue.scene('off')
                if (event.code == 63):
                    print ("menu button")
                    hue.scene('sofa_dimmed')
                if (event.code ==  1):
                    print ("back button")
                    hue.scene('tropical')
                if (event.code == 62):
                    print ("keyboard button")
                    hue.set_brightness("0", max(0,   hue.get_brightness("0") - 30))
                if (event.code == 64):
                    print ("reload button")
                    hue.set_brightness("0", min(255, hue.get_brightness("0") + 30))

device1 = evdev.InputDevice('/dev/input/event0')
print(device1)

device2 = evdev.InputDevice('/dev/input/event2')
print(device2)

p1 = Process(target=listen, args=(device1,))
p2 = Process(target=listen, args=(device2,))

p1.start()
p2.start()

p1.join()
p2.join()
