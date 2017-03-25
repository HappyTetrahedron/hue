import asyncio
import socket
import fcntl
import struct
from server_protocol import AlarmServerProtocol

def start_server(port):
    # Fancy python 3.5 stuff for async stuff
    loop = asyncio.get_event_loop()
    print("Starting UDP server on port: %d" % port)
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        AlarmServerProtocol,
        local_addr=('0.0.0.0', port))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()


