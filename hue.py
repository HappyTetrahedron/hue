#!/usr/bin/env python3

import requests
import json

def put_request(uri, keys):
    jdata = json.dumps(keys)
    r = requests.put("http://192.168.0.116/api/APIKEY/" + uri, jdata)

def get_request(uri):
    r = requests.get("http://192.168.0.116/api/APIKEY/" + uri)
    return json.loads(r.text)

def activate_scene(group, scene_key):
    keys = {"scene":scene_key}
    put_request("groups/"+group+"/action", keys)

def scene_random():
    activate_scene("1", "t-LfC4fk3s0IFbs")

def scene_focus():
    activate_scene("1", "hHq3iUPt1ADbmmM")

def scene_off():
    activate_scene("1", "xTLEreD08lNouvq")

def scene_night():
    activate_scene("1", "yvJum2ytSQt0eCM")

def scene_relax():
    activate_scene("1", "XLqfX-Z1g7cRqQb")

def scene_last():
    activate_scene("1", "KA3s3JfLTWqaq3F")

def scene_energize():
    activate_scene("1", "1SlwrM6xEfz-QnJ")

def scene_energize_fade():
    activate_scene("1", "aEiAPeVjkQ8wU5S")

def scene_sofa_dimmed():
    activate_scene("1", "3-Mwry4K2CXdjrI")

def set_brightness(group, bri):
    keys = {"bri":bri}
    put_request("groups/"+group+"/action", keys)

def get_brightness(group):
    r = get_request("groups/"+group)
    return r["action"]["bri"]

def set_to_color_hsb(light, color):
	keys = {"hue": + color[0], "sat": + color[1], "bri": color[2]}
	put_request("lights/"+light+"/state", keys)
