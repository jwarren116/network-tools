#!/usr/bin/env python
import socket
import email.utils
import mimetypes
import os


ROOT = os.path.join(os.getcwd(), 'webroot')


def response_ok(resolved_uri):
    """returns response message with headers, date and response"""
    response_code = "HTTP/1.1 200 OK"
    headers = "Content-Type: {}".format(resolved_uri[0])
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    response = "{}\r\n{}\r\n{}\r\n\r\n{}".format(
        response_code, date, headers, resolved_uri[1])
    return response


def response_error(code, reason):
    """formats errors raised to be returned to client"""
    response_code = "HTTP/1.1 {} {}".format(code, reason)
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: text/plain"
    response = u"{}\r\n{}\r\n{}\r\n\r\n{}".format(response_code, date,
                                                  headers, reason)
    return response


def parse_request(request):
    """parse request and return URI, errors raised for invalid protocols
    and requests
    """
    request = request.split('\r\n')
    first_line = request[0].split(' ')
    if first_line[0] != "GET":
        raise RequestError(405, "Method Not Allowed")
    elif first_line[2] != "HTTP/1.1":
        raise RequestError(505, "HTTP Version Not Supported")
    else:
        return first_line[1]


def resolve_uri(uri):
    """returns tuple of (content, body), if directory, returns listing of links,
    if not found, raises RequestError"""
    uri = uri.lstrip('/')
    if os.path.isdir(os.path.join(ROOT, uri)):
        body = os.listdir(os.path.join(ROOT, uri))
        dir_body = "<!DOCTYPE html><html><body><ul>"
        for item in body:
            dir_body = "{}<a href='{}'>{}</a></br>".format(
                dir_body, item, item)
        return ('text/html', dir_body)
    else:
        try:
            with open(os.path.join(ROOT, uri), 'rb') as file_handle:
                body = file_handle.read()
                return (mimetypes.guess_type(uri)[0], body)
        except IOError:
            raise RequestError(404, "Page Not Found")


class RequestError(BaseException):
    """returns appropriately formatted response error when raised"""
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason

    def __str__(self):
        return response_error(self.code, self.reason)


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
            try:
                parsed = parse_request(req)
                resolved = resolve_uri(parsed)
                response_msg = response_ok(resolved)
            except RequestError as error:
                response_msg = str(error)

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
