#!/usr/bin/env python3

import yaml
import json
import requests
import time
from xdg.BaseDirectory import *

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

while (not success):
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

keys = {'devicetype':devicetype}
response = [dict()]

while (not 'success' in response[0]):
	time.sleep(1)
	response = post_request(ip, "", keys)
	print(response)

cfg['api_key'] = response[0]['success']['username']

print("API key received")

scene_list = get_request(ip, cfg['api_key'] + "/scenes")

scenes = []
for scene_key, scene in scene_list.items():
	scene_dict = dict();
	scene_dict['scene'] = scene['name']
	scene_dict['group'] = 1 # TODO not sure how to find out properly
	scene_dict['key'] = scene_key
	scenes.append(scene_dict)

cfg['scenes'] = scenes

print("Scene info collected")

with open(xdg_config_dirs[0] + "/hue/hueconfig.yml", "w") as outfile:
	yaml.dump(cfg, outfile, default_flow_style=False)

print("Configuration stored to " + xdg_config_dirs[0] + "/hue/hueconfig.yml")
