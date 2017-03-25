#!/usr/bin/env python3

import hue
from PIL import Image
import ctypes
import os
import time
import colorsys
import sys
from optparse import OptionParser

# screenshot library constants
LibName = 'prtscn.so'
AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
grab = ctypes.CDLL(AbsLibPath)

# parse options
parser = OptionParser()
parser.add_option("-l", "--lights", dest="lightstr", default="1", action="store", type="string", help="comma-separated list of light IDs to control")
parser.add_option("-o", "--oversaturation", dest="Oversaturation", default=2, action="store", type="float", help="Factor by which saturation is multiplied")
parser.add_option("-b", "--brightnessdamping", dest="BrightnessFactor", default=0.2, action="store", type="float", help="Factor by which brightness is multiplied")
parser.add_option("-i", "--interval", dest="Interval", default=1, action="store", type="float", help="Time in seconds between sampling passes")
parser.add_option("-s", "--saturation_weight", dest="SatEnhance", default=10, action="store", type="float", help="Factor by which more saturated colors are preferred over desaturated ones")
parser.add_option("-w", "--width", dest="Width", default=1600, action="store", type="int", help="Witdth in pixels of the screen region to capture")
parser.add_option("-t", "--height", dest="Height", default=900, action="store", type="int", help="Height in pixels of the screen region to capture")
parser.add_option("-x", dest="X", default=0, action="store", type="int", help="X coordinate of the upper right corner of the sample region")
parser.add_option("-y", dest="Y", default=0, action="store", type="int", help="Y coordinate of the upper right corner of the sample region")
parser.add_option("-v", dest="Verbose", default=False, action="store_true", help="Verbosity")
(opts, args) = parser.parse_args()

lights = opts.lightstr.split(",")

def grab_screen(x1,y1,w,h):
    size = w * h
    objlength = size * 3

    grab.getScreen.argtypes = []
    result = (ctypes.c_ubyte*objlength)()

    grab.getScreen(x1,y1, w, h, result)
    return Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)

# adds up two three-tuples component wise
def add(t1, t2):
	return (t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2])

# divides a three-tuple by a constant
def div(t, c):
	return (t[0]/c, t[1]/c, t[2]/c)

# multiplies a three-tuple by a constant
def mul(t, c):
	return (t[0]*c, t[1]*c, t[2]*c)

# takes an RGB tuple and returns a HSV tuple
def rgb_to_hsv(rgb):
	rgb = div(rgb, 255)
	hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
	return hsv

# takes an RGB tuple and returns a color tuple suitable for hue lamps
def rgb_to_huecol(rgb):
	hsv = rgb_to_hsv(rgb)
	hue = (hsv[0] * 65545, hsv[1] * 255, hsv[2] * 255)
	hue = (int(round(hue[0])),int(round(hue[1])),int(round(hue[2])))
	return hue

# Calculates the weight of a color based on its RGB variance.
def get_weight(col):
	mean = (col[0] + col[1] + col[2]) / 3
	var = ( pow(col[0] - mean, 2) + pow(col[1] - mean, 2) + pow(col[2] - mean, 2) ) / 3 
	# return standard deviation. add 1 to prevent 0 weights
	return 1 + pow(var, 0.5)

# Calculates the weight of a color based on its saturation times the -s parameter
def get_hsv_weight(col):
    sat = rgb_to_hsv(col)[1]
    return 1 + sat * opts.SatEnhance

while True:
	# take screenshot
	img = grab_screen(opts.X,opts.Y,opts.Width,opts.Height)

	n = 0
	col = (0,0,0)

	# downsample vigorously and accumulate color values
	for x in range(0,opts.Width,10):
		for y in range(0,opts.Height,10):
			currentcol = img.getpixel((x,y))
			weight = get_hsv_weight(currentcol)
			col = add(col, mul(currentcol, weight))
			n += weight

	# get average color in hue lamp format
	col = div(col, n)
	huecol = rgb_to_huecol(col)

	if (opts.Verbose):
		print("Unmodified Color:", huecol)

	# modify color a little
	huecol = (huecol[0], min(255, int(round(huecol[1] * opts.Oversaturation))), min(255, int(round(huecol[2] * opts.BrightnessFactor))))

	if (opts.Verbose):
		print("Finalized  Color:", huecol)

	# set color
	for light in lights:
		hue.set_to_color_hsb(light, huecol)

	# wait a bit
	time.sleep(opts.Interval)
