from subprocess import call
import datetime

class AlarmServerProtocol:

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print("Received message")
        self.handle_message(data)

    def handle_message(self, data):
        print(data)

        strdata = data.decode("UTF-8")
        if (strdata == "none"):
            call(["/home/hue/alarmserver/clearat"])
        else:
            time = datetime.datetime.fromtimestamp( int(strdata)/1000 - 60 * 15 ).strftime('%y%m%d%H%M')
            call(["/home/hue/alarmserver/addat", time])
