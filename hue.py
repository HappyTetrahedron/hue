#!/usr/bin/env python3

import requests
import json
import yaml
import xdg

configdir = xdg.XDG_CONFIG_HOME


class Hue:
    def __init__(self, cfg=None):
        if cfg:
            self.cfg = cfg
        else:
            try:
                with open(str(configdir) + "/hue/hueconfig.yml", "r") as ymlfile:
                    self.cfg = yaml.load(ymlfile)
                    ymlfile.close()
            except FileNotFoundError:
                print("Configuration file not found! Please create your configuration. Hue will not work!")
        if 'scenes' not in self.cfg:
            self._fetch_scenes_to_config()

    def get_scene_info(self, scenename):
        for scene in self.cfg['scenes']:
            if scene['scene'] == scenename:
                return scene
        return {}

    def put_request(self, uri, keys):
        jdata = json.dumps(keys)
        r = requests.put("http://" + self.cfg['bridge_ip'] + "/api/" + self.cfg['api_key'] + "/" + uri, jdata)

    def get_request(self, uri):
        r = requests.get("http://" + self.cfg['bridge_ip'] + "/api/" + self.cfg['api_key'] + "/" + uri)
        return json.loads(r.text)

    def _fetch_scenes_to_config(self):
        scene_list = self.get_request("scenes")

        scenes = []
        for scene_key, scene in scene_list.items():
            scene_dict = dict()
            scene_dict['scene'] = scene['name']
            scene_dict['group'] = scene['group'] if scene['type'] == "GroupScene" else "0"
            scene_dict['key'] = scene_key
            scenes.append(scene_dict)

        self.cfg['scenes'] = scenes

    def get_lights(self, group=None):
        if group == None:
            r = self.get_request("lights")
            lights = r.keys()
        else:
            r = self.get_request("groups/%s" % group)
            lights = r['lights']
        return lights

    def get_groups(self, ):
        r = self.get_request("groups")
        groups = list(r.keys())
        groups.insert(0, "0")
        return groups

    def activate_scene(self, group, scene_key):
        keys = {"scene": scene_key}
        self.put_request("groups/%s/action" % str(group), keys)

    def scene(self, scenename):
        sceneinfo = self.get_scene_info(scenename)
        self.activate_scene(sceneinfo['group'], sceneinfo['key'])

    def set_brightness(self, group, bri):
        keys = {"bri":bri}
        self.put_request("groups/"+str(group)+"/action", keys)

    def set_light_brightness(self, light, bri):
        keys = {"bri":bri}
        self.put_request("lights/"+str(light)+"/state", keys)

    def get_light_brightness(self, light):
        r = self.get_request("lights/"+str(light))
        return r["state"]["bri"]

    def get_brightness(self, group):
        r = self.get_request("groups/"+str(group))
        return r["action"]["bri"]

    def set_to_color_hsb(self, light, color):
        keys = {"hue": + color[0], "sat": + color[1], "bri": color[2]}
        self.put_request("lights/"+str(light)+"/state", keys)

    def set_group_to_color_hsb(self, group, color):
        keys = {"hue": + color[0], "sat": + color[1], "bri": color[2]}
        self.put_request("groups/"+str(group)+"/action", keys)

    def set_to_color_temp(self, light, color):
        keys = {"ct": color}
        self.put_request("lights/"+str(light)+"/state", keys)

    def set_group_to_color_temp(self, group, color):
        keys = {"ct": color}
        self.put_request("groups/"+str(group)+"/action", keys)

    def turn_on(self, light):
        keys = {"on": True}
        self.put_request("lights/"+str(light)+"/state", keys)

    def turn_on_group(self, group):
        keys = {"on": True}
        self.put_request("groups/"+str(group)+"/action", keys)

    def turn_off(self, light):
        keys = {"on": False}
        self.put_request("lights/"+str(light)+"/state", keys)

    def turn_off_group(self, group):
        keys = {"on": False}
        self.put_request("groups/"+str(group)+"/action", keys)

    def is_group_on(self, group):
        status = self.get_request('groups/{}'.format(group))
        return status['state']['any_on']
