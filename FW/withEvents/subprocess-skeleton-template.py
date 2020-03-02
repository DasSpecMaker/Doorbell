import socketio
import subprocess
import time


sio = socketio.Client();
sio.connect('http://localhost:9000'); #can customize ip and port if you want
#localhost shouldnt have to be modified since the subprocesses are ran on the same pi.
#Streaming httpserver will runs on 8000 (streamTest.py)

#predefined event handler, occurs when successful connection
@sio.event
def connect():
    print("Connected")

#predefined event handler, occurs when connecting to server failed
@sio.event
def connect_error():
    print("The connection failed!")

#predefined event handler, occurs when it disconnects from server
@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('one_event') #the function directly underneath this statement is the event handler
def another_event(sid):
    print('one_event handler')
    sio.emit('thrown_event_without_data'); #emit a socketio event to raspberry pi server

@sio.on('two_event')
def another_event(sid,data): #if the event captured has data, add an extra object in parameter in order to manipulate and make use of it
    print('two_event handler')
    sio.emit('thrown_event_with_data',{'measure':'24'}); #emit a socket event with data to the raspberry pi server
    #data can be sent as a dictionary for python and JSON in JS