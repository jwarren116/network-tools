#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import email.utils


def response_ok(request):
    response_code = "HTTP/1.1 200 OK"
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: Text/HTML"
    response = "{}\r\n{}\r\n{}\r\n\r\n".format(response_code, date, headers)
    return response.encode('utf-8')


def response_error(code, reason):
    response_code = "HTTP/1.1 {} {}".format(code, reason)
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: Text/HTML"
    response = "{}\r\n{}\r\n{}\r\n\r\n".format(response_code, date, headers)
    return response.encode('utf-8')


def parse_request(request):
    pass


try:
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    while True:
        connection, client_address = server_socket.accept()
        buffsize = 4096
        req = ''
        done = False
        while not done:
            msg = connection.recv(buffsize)
            if len(msg) < buffsize:
                done = True
            req += msg
            # print "This is the request:"            
            # print req
            # print "----"

        # response_msg = parse_request(req)
        # print "This is the response I will send:"
        # print response_msg
        # print "----"
        connection.sendall(parse_request(req))

        # shutdown socket to writing after sending echo message
        connection.shutdown(socket.SHUT_WR)
        connection.close()
except KeyboardInterrupt:
    server_socket.close()
