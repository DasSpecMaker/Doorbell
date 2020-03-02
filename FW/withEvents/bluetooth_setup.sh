#!/bin/bash

#sudo apt-get update
#sudo apt-get upgrade

#sudo apt-get install bluez python-bluez python-bluetooth minicom sdptool bluetooth bluez-utils bluman python-serial python-dev libbluetooth-dev

sudo rfkill unblock all

sudo bash -c 'cat > /etc/systemd/system/dbus-org.bluez.service <<EOF
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1
ProtectHome=true
ProtectSystem=full

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service

EOF'

sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service

#reboot system to make sure its all there

sudo bash -c 'cat > /etc/bluetooth/rfcomm.conf <<EOF
rfcomm1 {
	#Automatically bind the device at startup
	bind yes;
	#Bluetooth address of the device
	device 24:6F:28:0B:BF:EE;

	#RFCOMM channel for the connection
	channel 1;

	#Description of the connection
	comment "Door_Unlocker";
}
EOF'

#sudo rfcomm bind all

#service bluetooth start
#echo -e "power on" | bluetoothctl 
#sleep 1
#echo -e "pairable on" | bluetoothctl 
#sleep 1
#echo -e "agent on" | bluetoothctl 
#sleep 1
#echo -e "default-agent" | bluetoothctl 
#sleep 1
#echo -e "scan on" | bluetoothctl | tee 
#sleep 40
#echo -e "pair 24:6F:28:0B:BF:EE" | bluetoothctl
#sleep 10
#echo -e "trust 24:6F:28:0B:BF:EE" | bluetoothctl
#sleep 5
#echo -e "connect 24:6F:28:0B:BF:EE" | bluetoothctl

sudo rfcomm connect hci0 24:6F:28:0B:BF:EE
