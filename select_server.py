#!/usr/bin/env python
import socket
import email.utils
import mimetypes
import os
import sys
import select


ROOT = os.path.join(os.getcwd(), 'webroot')


def response_ok(uri):
    resolved_uri = resolve_uri(uri)
    if resolved_uri[0] == 404:
        response_code = "HTTP/1.1 404 Not Found"
        headers = "Content-Type: text/plain"
    else:
        response_code = "HTTP/1.1 200 OK"
        headers = "Content-Type: {}".format(resolved_uri[0])

    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    response = "{}\r\n{}\r\n{}\r\n\r\n{}".format(
        response_code, date, headers, resolved_uri[1])
    return response


def response_error(code, reason):
    response_code = "HTTP/1.1 {} {}".format(code, reason)
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: Text/HTML"
    response = u"{}\r\n{}\r\n{}\r\n\r\n".format(response_code, date, headers)
    return response


def parse_request(request):
    request = request.split('\r\n')
    first_line = request[0].split(' ')
    if first_line[0] != "GET":
        return response_error(405, "Method Not Allowed")
    elif first_line[2] != "HTTP/1.1":
        return response_error(505, "HTTP Version Not Supported")
    else:
        return response_ok(first_line[1])


def resolve_uri(uri):
    uri = uri.lstrip('/')
    content = mimetypes.guess_type(uri)
    if content[0] is None:
        body = os.listdir(os.path.join(ROOT, uri))
        dir_body = "<!DOCTYPE html><html><body><ul>"
        for item in body:
            dir_body = "{}<a href='{}'>{}</a></br>".format(
                dir_body, item, item)
        return (content[0], dir_body)
    else:
        try:
            with open(os.path.join(ROOT, uri), 'rb') as file_handle:
                body = file_handle.read()
                return (content[0], body)
        except IOError:
            return (404, "404 - Page Not Found")


def server(log_buffer=sys.stderr):
    buffsize = 32
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(5)

    input = [server_socket, sys.stdin]
    running = True

    while running:
        read_ready, write_ready, except_read = select.select(input, [], [], 0)
        for readable in read_ready:
            if readable is server_socket:
                # create new handler sockets as clients connect
                handler_socket, address = readable.accept()
                input.append(handler_socket)

            elif readable is sys.stdin:
                # terminates server on stdin
                sys.stdin.readline()
                running = False

            else:
                # this socket is a handler socket created by client connection
                req = ''
                done = False
                while not done:
                    data = readable.recv(buffsize)
                    if len(data) < buffsize:
                        done = True
                    req += data
                response = parse_request(req)
                readable.sendall(response)
                readable.close()
                input.remove(readable)

    server_socket.close()


if __name__ == '__main__':
    server()
    sys.exit(0)
