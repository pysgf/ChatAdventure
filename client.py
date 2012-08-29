#!/usr/bin/env python2.7

import socket
import sys
import argparse
import hashlib
import random

from protocol import *


def message_loop(sock, connection, key):
    running = True

    while running:
        received = sock.recv(1024)
        print "server:", received

        print received
        if BYE_RE.match(received):
            running = False
        else:
            message = raw_input("you say: ")
            if message:
                sock.sendto(MESSAGE.format(key=key, message=message), connection)


def main(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    name = raw_input("enter your login: ").strip()
    key = hashlib.sha1(str(random.getrandbits(128))).hexdigest()

    try:
        sock.sendto(HELLO.format(name=name, key=key), (host, port))

        message_loop(sock, (host, port), key)

    finally:
        sock.close()

    print "server said: ", received


if __name__=='__main__':
    # TODO: parse args here

    host = "localhost"
    port = 8123
    main(host=host, port=port)

