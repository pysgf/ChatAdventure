#!/usr/bin/env python2.7

import SocketServer
import argparse

from protocol import *


class HandleTCP(SocketServer.BaseRequestHandler):

    def handle(self):
        while 1:
            data = self.request.recv(1024).strip()
            if not data:
                break

            print "client:", data
            self.request.sendall(data)


def main(port):
    HOST, PORT = "0.0.0.0", port
    server = SocketServer.TCPServer((HOST, PORT), HandleTCP)
    server.serve_forever()


if __name__=='__main__':
    # TODO: parse args here

    port = 8123
    main(port=port)
