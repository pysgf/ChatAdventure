#!/usr/bin/env python2.7

import SocketServer
import argparse

from protocol import *


clients = {}

def broadcast(message):
    print "broadcasting:", message
    for key, info in clients.items():
        info['sock'].sendto(message, info['addr'])


class Handler(SocketServer.BaseRequestHandler):

    def handle(self):
        packet, socket = self.request

        if not packet:
            return

        message = HELLO_RE.match(packet)
        if message:
            data = message.groupdict()
            clients[data['key']] = {
                    'name': data['name'],
                    'addr': self.client_address,
                    'sock': socket
            }

            broadcast("{0} logged in, say hello!".format(data['name']))
            return

        message = MESSAGE_RE.match(packet)
        if message:
            data = message.groupdict()
            if data['key'] in clients:
                client = clients[data['key']]
                broadcast("{0} said: {1}".format(client['name'], data['message']))
                return

        print 'could not understand: "{0}"'.format(packet)


def main(port):
    HOST, PORT = "0.0.0.0", port
    server = SocketServer.UDPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__=='__main__':
    # TODO: parse args here

    port = 8123
    main(port=port)

