import subprocess
import time
import socketio

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

@sio.on('NFC') #the function directly underneath this statement is the event handler
def Activate_NFC(sid):
    print('NFC_is_Active')
    sio.emit('NFC_is_Scanning'); #emit a socketio event to raspberry pi server
    subprocess.call('./nfc.py') #must state the location of nfc.py and nfc_auth.txt must be in same location or specified location

