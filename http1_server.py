#!/usr/bin/env python
import socket
import email.utils


def response_ok(request):
    response_code = "HTTP/1.1 200 OK"
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: Text/HTML"
    response = "{}\r\n{}\r\n{}\r\n\r\n".format(response_code, date, headers)
    return response


def response_error(code, reason):
    response_code = "HTTP/1.1 {} {}".format(code, reason)
    date = "Date: {}".format(email.utils.formatdate(usegmt=True))
    headers = "Content-Type: Text/HTML"
    response = u"{}\r\n{}\r\n{}\r\n\r\n".format(response_code, date, headers)
    return response.encode('utf-8')


def parse_request(request):
    request = request.split('\r\n')
    first_line = request[0].split(' ')
    if first_line[0] != "GET":
        return response_error(405, "Method Not Allowed")
    elif first_line[2] != "HTTP/1.1":
        return response_error(505, "HTTP Version Not Supported")
    else:
        return response_ok(first_line[1])


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
