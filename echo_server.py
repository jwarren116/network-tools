import socket


try:
    while True:
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)
        server_socket.bind(('127.0.0.1', 50000))
        server_socket.listen(1)
        connection, client_address = server_socket.accept()

        # receive message from client, and immediately return
        echo_msg = connection.recv(16)
        connection.sendall(echo_msg)

        # shutdown socket to writing after sending echo message
        connection.shutdown(socket.SHUT_WR)
        connection.close()

except KeyboardInterrupt:
    server_socket.close()
