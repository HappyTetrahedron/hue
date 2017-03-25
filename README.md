# A collection of scripts to control Philips Hue lights

This repo contains a collection of programs which can be used to control
Philips Hue lights. At the core of these is a python script which acts as an
interface between the other scripts and the Philips Hue API (hue.py).


## colors.py

cycles through all colors


## ambilight.py

lets your hue lights mimic the color on your display

## hueremote.py

listens to an USB remote (or keyboard) and maps the buttons to light scenes

## alarmserver

works with (AlarmDroid)[https://github.com/Jereviendrai/alarmdroid] to turn on your lights when your phone alarm rings.
