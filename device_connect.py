import serial
import subprocess
import numpy as np
import sys
import glob

#commands are [hcitool scan, sudo rfcomm bind 0 device address]


class device_connect():

    def __init__(self):
        print("checking bluetooth devices in range")

    def check_devices(self):
        #create empty dictionary to store bluetooth devices that are on and in range
        hc_devices = []
        #create empty dictionary to store arduiino that is collecting load cell data
        weigh_devices = {}
        #call subprocess to get adalogger device info and store in dictionary {device:device address}
        devices = subprocess.check_output("bluetoothctl devices", shell=True)
        devices = devices.decode('utf-8').split('\n')
        devices = [x for x in devices if 'HC-05' in x or 'HC-06' in x]
        devices = [x.replace('Device ', '') for x in devices]
        devices = [x.split(' ') for x in devices]

        #get connected USB devices and connect
        weigh_devices = glob.glob('/dev/ttyUSB*')

        for i in np.arange(0,len(devices)):
            hc_devices.append(devices[i][0])

        if not bool(hc_devices) == True:
            print("No devices available")
            sys.exit(0)

        return hc_devices, weigh_devices

    def bind_address(self,hc_devices):
        #if any rfcomm files present, unbind to start new binding session
        subprocess.run("echo 1nickhong123| sudo rfcomm release rfcomm0", shell=True)

        i_ada = 0
        for key in hc_devices:
            subprocess.run("echo 1nickhong123| sudo rfcomm bind {} {}".format(i_ada, key), shell=True)
            i_ada+=1









