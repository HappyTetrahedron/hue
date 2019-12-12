#!/usr/bin/env python

from optparse import OptionParser
from flask import Flask
from flask import request
from subprocess import call

import datetime
import yaml


app = Flask(__name__)
config = None


@app.route("/time", methods=['POST'])
def handle_request():
    data = request.get_json()
    print(data)
    if 'next_alarm' in data:
        time = datetime.datetime.fromtimestamp( data['next_alarm']/1000 - 60 * 15 ).strftime('%y%m%d%H%M')
        call([config["addat_path"], time])
    else:
        call([config["clearat_path"]])


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config', default='config.yml', type='string',
                      help="Path of configuration file")
    (opts, args) = parser.parse_args()
    with open(opts.config, 'r') as configfile:
        config = yaml.load(configfile)

    if 'ssl' in config:
        app.run(config['host'], config['port'], ssl_context=(config['ssl']['cert_path'], config['ssl']['key_path']))
    else:
        app.run(config['host'], config['port'])
