#if no audio in jack, go to "sudo raspi -config", Advanced options, Audio, and select 3.5 Audio Jack

#type "alsamixer", select sound card PnP USB, increase Mic Volume

#speaker-test -t wav


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
    exit()

@sio.on('AudioRecod') #the function directly underneath this statement is the event handler
def record_event(sid):
    print('Audio_Recording')
    sio.emit('Started_Audio_Recording'); #emit a socketio event to raspberry pi server
    #record using usbmic
    subprocess.call("arecord --device=hw:1,0 --formatS16_LE --rate 44100 -V mono -c1 voice.wav", shell=True)







