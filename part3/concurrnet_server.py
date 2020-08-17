import socket
import time
import os

"""
    This simples way to make concurrent server is to use the fork unix system call.
    The kernel uses descriptor reference counts to decide 
    whether to close the file/socket or not.

    * make sure to close duplicate socket descriptors
"""

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    time.sleep(20)  # sleep and block the process for 60 seconds


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print("server is listning on port", PORT)

    while True:
        client_connection, client_address = listen_socket.accept()
        pid = os.fork()
        if pid == 0: # child
            print('Serving HTTP on port {} processs ID {} ...'.format(PORT, os.getpid()))
            listen_socket.close() # close child copy
            handle_request(client_connection)
            client_connection.close()
        else:
            # close client connection b/c child is handling that request
            # and keep listining for more connections
            client_connection.close() 

if __name__ == '__main__':
    serve_forever()
