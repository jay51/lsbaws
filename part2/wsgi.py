import socket
import io
import sys


class WSGI:
    addr_family = socket.AF_INET
    sock_tyep = socket.SOCK_STREAM
    request_queue = 1

    def __init__(self, server_addr):
        self.listen_sock = socket.socket(addr_family, sock_type)
        # allow to reuse same addr and port
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_addr)

        listen_socket.listen(request_quere)
        host, port = listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        print(self.server_name)
        self.headers_set = []
    
    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        while True:
            self.client_conn, client_addr = self.listen_sock.accept()
            self.handle_one_rquest()
    
    def handle_one_request(self):
        self.request_data = self.client_conn.recv(1024)
        self.request_data = self.request_data.decode("utf-8")
        print(''.join(
            f'< {line}\n' for line in self.request_data.splitlines()
        ))

        self.parse_data(self.request_data)
        # Construct environment dictionary using request data
        env = self.get_environ()
        result = self.application(env, self.start_response) # what is self.start_response
        self.finish_response(result)

    def parse_request(self):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Break down the request line into components
        (self.request_method,  # GET
        self.path,            # /hello
        self.request_version  # HTTP/1.1
        ) = request_line.split()



    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env


    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Mon, 15 Jul 2020 5:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. for simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response


    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
        
            for data in result:
                response += data.decode("utf-8")
            # Print formatted response data a la 'curl -v'
            print(''.join(
                f'> {line}\n' for line in response.splitlines()
            ))

            response_bytes = response.encode()
            self.clien_conn.sendall(response_bytes)
        finally:
            self.client_conn.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888


def make_server(server_address, application):
    server = WSGI(server_address)
    server.set_app(application)
    return server


def main():
    if len(sys.argv) < 2:
        sys.exit("Provide a WSGI application object as module:callable")

    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module) # to import things at runtime
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()




