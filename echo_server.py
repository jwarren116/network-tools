import socket


try:
    while True:
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

        address = ('127.0.0.1', 50000)
        server_socket.bind(address)
        server_socket.listen(1)

        connection, client_address = server_socket.accept()
        echo_msg = connection.recv(16)

        connection.sendall(echo_msg)
        connection.shutdown(socket.SHUT_WR)

except KeyboardInterrupt:
    return "Connection closing..."
    connection.close()
