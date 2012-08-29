#!/usr/bin/env python2.7

import socket
import sys
import argparse

from protocol import *


def message_loop(sock):
    running = True

    while running:
        received = sock.recv(1024)
        print "server:", received

        if received == BYE:
            running = False
        else:
            message = raw_input("you say: ")
            sock.sendall(MESSAGE.format(message=message))


def main(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    name = raw_input("enter your login: ").strip()

    try:
        sock.connect((host, port))
        sock.sendall(HELLO.format(name=name))

        message_loop(sock)

    finally:
        sock.close()

    print "server said: ", received


if __name__=='__main__':
    # TODO: parse args here

    host = "localhost"
    port = 8123
    main(host=host, port=port)
