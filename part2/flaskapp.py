from flask import Flask
from flask import Response
server = Flask('flaskapp')


# run like this: python server.py flaskapp:app
@server.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )

app = server.wsgi_app
