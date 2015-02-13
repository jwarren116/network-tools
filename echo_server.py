# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import socket


def server():
    try:
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)
        server_socket.bind(('127.0.0.1', 50000))
        server_socket.listen(1)

        while True:
            connection, client_address = server_socket.accept()
            buffsize = 32
            response_msg = ''
            done = False
            while not done:
                echo_msg = connection.recv(buffsize)
                if len(echo_msg) < buffsize:
                    done = True
                response_msg += echo_msg
                print response_msg
            connection.sendall(response_msg.encode('utf-8'))

            # shutdown socket to writing after sending echo message
            connection.shutdown(socket.SHUT_WR)
            connection.close()

    except KeyboardInterrupt:
        server_socket.close()

if __name__ == '__main__':
    server()
