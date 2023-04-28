import eventlet
from recognition import app
import socketio
from waitress import serve

sio = socketio.Server()
appServer = socketio.WSGIApp(sio, app)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    #Multiple clients can connect to either localhost at port 8080 or the machine's local_ip:8080
    print('connect at : http://localhost:8080 or http://local_ip:8080')
    serve(app=app, host='0.0.0.0', port=8080, url_scheme='HTTP', threads=6)
    """
    This is the old way of connecting to the server that didn't support multiple clients
    Eventlet also printed a trace error whenever the client would disconnect but serve does not
    """
    #eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), appServer)