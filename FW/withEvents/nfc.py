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

@sio.on('Activate_NFC') #the function directly underneath this statement is the event handler
def Activate_NFC(sid):
    print('NFC_is_Active')
    sio.emit('NFC_is_Scanning'); #emit a socketio event to raspberry pi server
    subprocess.call("nfc_run()", shell=True)





def nfc_raw():
    lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
    return lines

def read_nfc():
    lines=nfc_raw()
    return lines

def run():
    try:
     #while True:
        myLines=read_nfc()
        buffer=[]
        for line in myLines.splitlines():
            line_content=line.split()
            if(not line_content[0] == 'UID'):
                pass
            else:
                buffer.append(line_content)
        str=buffer[0]
        id_str=str[2]+str[3]+str[4]+str[5]
        print (id_str)

        fo = open("nfc_auth.txt", "r") 
        file_contents = fo.read()
        Flag = 0
        for i in file_contents.split('\n'):
            if id_str == i:
                Flag = 1
        if Flag == 1:
            print('Access Granted')
            subprocess.call("speaker-test -t wav", shell=True) #audio code goes here
        else :
            print('Access Denied')
            

    except KeyboardInterrupt:
        pass
