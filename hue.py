#!/usr/bin/env python3

import requests
import json
import yaml
from xdg.BaseDirectory import *

configdir = xdg_config_dirs[0]

try:
    with open(configdir + "/hue/hueconfig.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        ymlfile.close()
except FileNotFoundError:
    print("Configuration file not found! Please create your configuration. Hue will not work!")

def get_scene_info(scenename):
    for scene in cfg['scenes']:
        if scene['scene'] == scenename:
            return scene
    return []

def put_request(uri, keys):
    jdata = json.dumps(keys)
    r = requests.put("http://" + cfg['bridge_ip'] + "/api/" + cfg['api_key'] + "/" + uri, jdata)

def get_request(uri):
    r = requests.get("http://" + cfg['bridge_ip'] + "/api/" + cfg['api_key'] + "/" + uri)
    return json.loads(r.text)

def get_lights(group=None):
    if group == None:
        r = get_request("lights")
        lights = r.keys()
    else:
        r = get_request("groups/%s" % group)
        lights = r['lights']
    return lights

def get_groups():
    r = get_request("groups")
    groups = list(r.keys())
    groups.insert(0, "0")
    return groups

def activate_scene(group, scene_key):
    keys = {"scene":scene_key}
    put_request("groups/%s/action" % str(group), keys)

def scene(scenename):
    sceneinfo = get_scene_info(scenename)
    activate_scene(sceneinfo['group'], sceneinfo['key'])

def set_brightness(group, bri):
    keys = {"bri":bri}
    put_request("groups/"+str(group)+"/action", keys)

def set_light_brightness(light, bri):
    keys = {"bri":bri}
    put_request("lights/"+str(light)+"/state", keys)

def get_light_brightness(light):
    r = get_request("lights/"+str(light))
    return r["state"]["bri"]

def get_brightness(group):
    r = get_request("groups/"+str(group))
    return r["action"]["bri"]

def set_to_color_hsb(light, color):
	keys = {"hue": + color[0], "sat": + color[1], "bri": color[2]}
	put_request("lights/"+str(light)+"/state", keys)

def set_group_to_color_hsb(group, color):
	keys = {"hue": + color[0], "sat": + color[1], "bri": color[2]}
	put_request("groups/"+str(group)+"/action", keys)

def set_to_color_temp(light, color):
	keys = {"ct": color}
	put_request("lights/"+str(light)+"/state", keys)

def set_group_to_color_temp(group, color):
	print("setting to %d" % color)
	keys = {"ct": color}
	import pprint
	pprint.pprint(keys)
	put_request("groups/"+str(group)+"/action", keys)

def turn_on(light):
    keys = {"on": True}
    put_request("lights/"+str(light)+"/state", keys)

def turn_on_group(group):
    keys = {"on": True}
    put_request("groups/"+str(group)+"/action", keys)

def turn_off(light):
    keys = {"on": False}
    put_request("lights/"+str(light)+"/state", keys)

def turn_off_group(group):
    keys = {"on": False}
    put_request("groups/"+str(group)+"/action", keys)

