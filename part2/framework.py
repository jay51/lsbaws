

"""
    framework app function use the environ object to decide the routing and
    other things. Then it calles start_response passing all the headers from
    the framework. Then return a response body
"""
# run like this: python server.py framework:app
def app(environ, start_response):
    """A barebones WSGI application.
        This is a starting point for your own Web framework :)
    """
    status = "200 ok"
    response_headers = [("Content-Type", "text/plain")]
    start_response(status, response_headers)
    return [b'Hello world from a simple WSGI application!\n']
