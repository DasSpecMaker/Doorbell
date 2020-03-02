#Must run ./bluetooth_setup first to create open channel


import bluetooth
import serial
import time
import subprocess
import socketio

#target_name = "Door_Unlocker"
#target_address = "24:6F:28:0B:BF:EE"



#print("Searching...")

#while 1:
#    result = bluetooth.lookup_name('24:6F:28:0B:BF:EE', timeout=20)
#    if(result ==None):
#        print "not found"
#    else:
#        print "Bluetooth device found"
#        break


#nearby_devices = bluetooth.discover_devices(lookup_names=True)
#print ("Found {} devices.".format(len(nearby_devices)))

#for addr, name in nearby_devices:
#    print(" {} - {}".format(addr, name))



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




#open_BT_Channel must run in order to lock or unlock
@sio.on('open_BT_Channel') #the function directly underneath this statement is the event handler
def open_BT_Channel(sid):
    print('Openning_Channel_for_BT_Connection')
    sio.emit('Channel_Open'); #emit a socketio event to raspberry pi server
    subprocess.call("./bluetooth_setup", shell=True) #run bluetooth_setup.sh




#UNLOCK
@sio.on('unlock_door') #the function directly underneath this statement is the event handler
def unlock_door(sid):
    print('Door_is_being_Unlocked')
    subprocess.call("echo 'u' | sudo minicom -b 9600 -o -D /dev/rfcomm0 -C test.txt", shell=True)
    f = open ('test.txt')
    lineList = f.readlines()
    f.close()
    sio.emit(lineList[-1]); #emit a socketio event to raspberry pi server
    time.sleep(2)

#LOCK
@sio.on('lock_door') #the function directly underneath this statement is the event handler
def lock_door(sid):
    print('Door_is_being_Locked')
    subprocess.call("echo 'l' | sudo minicom -b 9600 -o -D /dev/rfcomm0 -C test.txt", shell=True)
    f = open ('test.txt')
    lineList = f.readlines()
    f.close()
    sio.emit(lineList[-1]); #emit a socketio event to raspberry pi server
	time.sleep(2)





