import socket
import time
import os
import signal
import errno

"""
    This simples way to make concurrent server is to use the fork unix system call.
    * make sure to close duplicate socket descriptors

    The kernel uses descriptor reference counts to decide 
    whether to close the file/socket or not.

    If you don't close duplicate descriptors, the clients won't terminate because the client connections won't get closed.
    If you don't close duplicate descriptors, your long-running server will eventually run out of available file descriptors (max open files).
    When you fork a child process and it exits and the parent process doesn't wait for it and doesn't collect its termination status, it becomes a zombie.
    Zombies need to eat something and, in our case, it's memory. Your server will eventually run out of available 
    processes (max user processes) if it does't take care of zombies. You can't kill a zombie, you need to wait for it.
"""

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    # don't print inside signal handler because it's not safe. 
    # you could get many signals at one time which interupt the print causing unwanted behievor.
    # print('Child {pid} terminated with status {status}' '\n'.format(pid=pid, status=status))
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except OSError:
                return
        if pid == 0:
                return

            
    pid, status = os.wait()




def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    time.sleep(5)  # sleep and block the process for 60 seconds


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    signal.signal(signal.SIGCHLD, grim_reaper)
    print("server is listning on port", PORT)

    while True:
        # if accept gets interupted by the signal interupt, continue the loop to reaccept again
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.ENTIR: continue
            else: raise
            
        pid = os.fork()
        if pid == 0: # child
            print('Serving HTTP on port {} processs ID {} ...'.format(PORT, os.getpid()))
            listen_socket.close() # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            # close client connection b/c child is handling that request
            # and keep listining for more connections
            client_connection.close() 

if __name__ == '__main__':
    serve_forever()
