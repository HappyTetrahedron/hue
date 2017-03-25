# A collection of scripts to control Philips Hue lights

This repo contains a collection of programs which can be used to control
Philips Hue lights. At the core of these is a python script which acts as an
interface between the other scripts and the Philips Hue API (`hue.py`).

The file hueconfig.yml is used to configure hue.py. you need to specify the ip
address of your Hue bridge, your Hue API key, and the information for your
light scenes.

## colors.py

cycles through all colors


## ambilight.py

lets your hue lights mimic the color on your display.

You need to compile the included c program to a shared object file using

    gcc -shared -O3 -lX11 -fPIC -Wl,-soname,prtscn -o prtscn.so prtscn.c

The resulting `prtscn.so` file should be in the same directory as the `ambilight.py` script.

## hueremote.py

listens to an USB remote (or keyboard) and maps the buttons to light scenes

## alarmserver

works with [AlarmDroid](https://github.com/Jereviendrai/alarmdroid) to turn on your lights when your phone alarm rings.
