import socket

HOST, PORT = "localhost", 3000
DATA_LIMIT = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allow for port reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print(f"server listening on {HOST}:{PORT} ")

while True:
    client_conn, client_addr = sock.accept()
    client_data = client_conn.recv(DATA_LIMIT)
    print(client_data.decode("utf-8"))

    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_conn.sendall(http_response)
    client_conn.close()
