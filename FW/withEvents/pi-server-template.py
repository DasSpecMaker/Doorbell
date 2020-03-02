import time
import eventlet
import socketio
import threading
import subprocess
import signal

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
#start hardware subprocesses via linux commands
#streaming = subprocess.Popen(["python3","./subprocesses/streaming.py"])
#ultrasonic = subprocess.Popen(["python3","./subprocesses/hcsr04.py"])
#button = subprocess.Popen(["python3","./subprocesses/button.py"])

@sio.event
def connect(sid, environ):
    print('connection: ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
@sio.on('button_press')
def another_event(sid):
    print('button_press_recieved')
    sio.emit('button_press_recieved')

@sio.on('another_event_name')
def another_event(sid):
    print('Button was pressed, received emit')
    sio.emit('server_thrown_event');

@sio.on('event_with_data')
def another_event(sid,data):
    print('Printing data out');
    print(data)
    sio.emit('server_thrown_event_with_data',data);

#The server will bind to your pi's LAN ip and port 9000.
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 9000)), app)
    #app.run(threaded=True)
