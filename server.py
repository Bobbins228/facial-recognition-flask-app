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
    #socketio
    print('connect at : http://localhost:8080')
    serve(app=app, host='0.0.0.0', port=8080, url_scheme='HTTP', threads=6)
    #eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), appServer)