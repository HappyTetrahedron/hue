#!/usr/bin/env python3

import hue
import time
from optparse import OptionParser

# parse options
parser = OptionParser()
parser.add_option("-l", "--lights", dest="lightstr", default="1,2,3", action="store", type="string", help="comma-separated list of light IDs to control")
parser.add_option("-b", "--brightness", dest="brightness", default=255, action="store", type="int", help="Brightness")
parser.add_option("-s", "--saturation", dest="saturation", default=255, action="store", type="int", help="Saturation")
parser.add_option("-i", "--interval", dest="interval", default=5, action="store", type="int", help="Interval by which color ismodified each second. range: 1 - 100")
parser.add_option("-o", "--offset", dest="offset", default=0, action="store", type="int", help="offset between lights. range: 0 - 100")
parser.add_option("-v", dest="verbose", default=False, action="store_true", help="Verbosity")
(opts, args) = parser.parse_args()

lights = opts.lightstr.split(",")


hueval = 0
interval = int(round(opts.interval * 65535 / 100))
offset = int(round(opts.offset * 65535 / 100))
while True:
    if opts.verbose:
        print("color:", hueval)
    hueval = (hueval + interval) % 65535
    i = 0
    for light in lights:
        hue.set_to_color_hsb(light, [(hueval + i * offset) % 65535, opts.saturation, opts.brightness])
        i = i + 1
    time.sleep(.5)
