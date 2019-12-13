#!/usr/bin/env python3

import yaml
import json
import requests
import time
import hue
import xdg
import os


def get_request(ip, uri):
    r = requests.get("http://" + ip + "/api/" + uri)
    return json.loads(r.text)


def post_request(ip, uri, keys):
    jdata = json.dumps(keys)
    r = requests.post("http://" + ip + "/api/" + uri, jdata)
    return json.loads(r.text)


print("Welcome to the hue configuration generation tool!")

cfg = dict()

success = False

while not success:
    print("Please enter your Hue bridge IP address:")
    ip = input()
    try:
        get_request(ip, "0000")
    except:
        success = False
        print("Could not resolve address. Please try again.")
    else:
        success = True

cfg['bridge_ip'] = ip


print("Please enter a name for this configuration:")

devicetype = input()

print("Please press the blue push link button on your Hue bridge.")

success = False

keys = {'devicetype': devicetype}

response = [dict()]

while 'success' not in response[0]:
    time.sleep(1)
    response = post_request(ip, "", keys)
    print(response)

cfg['api_key'] = response[0]['success']['username']

print("API key received")

hue = hue.Hue(cfg)

print("Scene info collected")

basedir = str(xdg.XDG_CONFIG_HOME)
if not os.path.exists(basedir + "/hue"):
    os.mkdir(basedir + "/hue")

with open(basedir + "/hue/hueconfig.yml", "w") as outfile:
    yaml.dump(cfg, outfile, default_flow_style=False)

print("Configuration stored to " + basedir + "/hue/hueconfig.yml")
