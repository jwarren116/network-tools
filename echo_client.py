import socket
import sys


def client(msg):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    buffer = 16

    # sends command line message to server, closes socket to writing
    client_socket.sendall(msg)
    client_socket.shutdown(socket.SHUT_WR)

    response = client_socket.recv(16)
    while len(response) >= buffer:
        # receives and prints incoming echo response, then closes connection
        response += client_socket.recv(16)
    print response
    client_socket.close()


if __name__ == '__main__':
    client(sys.argv[1])
