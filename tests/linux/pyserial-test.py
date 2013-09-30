#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
pyserial-test.py

This will send and receive to the bluetooth devices.
It seems to work with protocol_3 at 115200 on both linvor and BlueSmirf
usage:
 to use the BlueSmirf
 $ ./pyserial-test.py
 or
 to use the linvor
 $ ./pyserial-test.py "linvor"
"""
import serial, time, sys

# these are ok by default
#dataBits = 1
#stopBits = 1
#parity = serial.PARITY_NONE

# need to set baud rate and timeout
baudRate = 115200
readTimeout = 0 

# which device ports to use
linvorPort = "/dev/rfcomm1"  #linvor
smirfPort  = "/dev/rfcomm0"  #bluesmirf

dataInit = ['02255',
            '03255',
            '09255100001225511255'
            ]

dataCycle = ['09255' 
             '09000'
             ]
cycleDelay  = 0.2

noReadLimit = 100

def init(btPort = smirfPort):
    connected = False
    while (not connected):
        ser = serial.Serial(port=btPort,baudrate=baudRate,timeout=0) #readTimeout)
        ser.open()
        connected = ser.isOpen()
        if(connected):
            print 'Connected.'
        else:
            print 'Not Connected.'
    return ser
        
def readStuff(ser, inCount):
    something = False
    count = inCount 
    nothingCount = 0
    while (something or count == inCount):
        got = ser.read(6)
        something = (len(got) > 0)
        if something:
            print str(count) + ': read: ' + got
            count += 1
            nothingCount = 0
        else:
            print 'nothing read'
            nothingCount +=1
        if nothingCount > noReadLimit:
            print 'exit on nothing read'
            exit()
    return count

def main():
    if len(sys.argv)>1 and  (sys.argv[1] == "linvor"):
        ser = init(linvorPort)
    else:
        ser = init()

    for d in dataInit :
        print str(0) + ': writing: ' + d 
        ser.write(d)
        time.sleep(0.2)
    count = readStuff(ser, 0)

    i = 0
    while(True):
        print str(count) + ': writing: ' + dataCycle[i] 
        ser.write(dataCycle[i])
        time.sleep(cycleDelay)
        count = readStuff(ser, count+1)
        i = (i + 1) % len(dataCycle)



if __name__ == '__main__':
    main()




