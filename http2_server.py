#!/usr/bin/env python
import socket
import email.utils
import mimetypes
import os


ROOT = os.path.join(os.getcwd(), 'webroot')


def response_ok(uri):
    # send URI to be resolved
    # include appropriate header reflecting correct content
    # add body from appropriate resource

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
    # take URI from response_ok, return tuple of (content-type, body)
    # if URI is directory, return listing of the directory (links)
    # if URI not found, return 404
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


def server():
    print "Serving files from: {}".format(ROOT)
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

            # send full request to parser, prints request and response
            response_msg = parse_request(req)
            print "REQUEST: {}".format(req)
            print "RESPONSE: \n{}\n--end--".format(response_msg)
            connection.sendall(response_msg)

            # shutdown socket to writing after sending echo message
            connection.shutdown(socket.SHUT_WR)
            connection.close()
    except KeyboardInterrupt:
        # close socket completely on interupt
        server_socket.close()


if __name__ == '__main__':
    server()
