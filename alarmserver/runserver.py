#!/usr/bin/env python3

import argparse
from server import start_server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
            '--port', type=int, #action='store_const', dest='port',
            help='portnumber(default: 6789)')

    args = parser.parse_args()

    if not args.port:
        port = 7887
    else:
        port = args.port

    start_server(port)

