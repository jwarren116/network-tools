#!/usr/bin/env python

from __future__ import unicode_literals
import socket
import sys


test_get = "GET /index.html HTTP/1.1"


def client(msg):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))

    # sends command line message to server, closes socket to writing
    client_socket.sendall(msg)
    client_socket.shutdown(socket.SHUT_WR)

    buffsize = 32
    response_msg = ''
    done = False
    while not done:
        msg_part = client_socket.recv(buffsize)
        if len(msg_part) < buffsize:
            done = True
            client_socket.close()
        response_msg += msg_part

    print response_msg
    return response_msg


if __name__ == '__main__':
    client(sys.argv[1])
