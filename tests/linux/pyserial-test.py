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

minDelay = 0.05  # the min time to wait after a send before checking for a read
connectDelay = 5  # when the device is opened, giveit time to start up??

writeChunkSize = 5
readChunkSize = 6

dataInit = [#'02255',
            #'03255',
            #'09255',
            '04255',
            '05255',
            '10000',
            '12255',
            '11255'
            ]

dataCycle = ['09255', 
             '09000'
             ]
cycleDelay  = 0.1 # the pause time between elements in the dataCycle

noReadLimit = 10 # how many empty reads before exiting

def init(btPort): # = smirfPort):
    # keep trying to open the rfcomm device until success
    # return the serial object
    connected = False
    while (not connected):
        ser = serial.Serial(port=btPort,baudrate=baudRate,timeout=readTimeout)
        ser.open()
        connected = ser.isOpen()
        if(connected):
            time.sleep(connectDelay)
            print 'Connected.'
        else:
            print 'Not Connected.'
    return ser
        
def readStuff(ser, inCount, nbReads):
    # read nbReads from ser obj, with the current counter at inCount, 
    # return the new current counter if something got read (will always, or crash)
    readLimit = readChunkSize * nbReads
    stuff = ""
    while (len(stuff) < readLimit):
        got = ser.read(6)
        if len(got) > 0:
            stuff += got 

    inc = 0
    if stuff != "":
        inc = 1
    print str(inCount+inc) + ': read: ' + stuff
    return inCount+inc

def setup(serObj):
    # sends all the elements in the dataInit, then reads the reply
    # returns the id-number of last read
    count = 0
    dataWrote = ""
    for d in dataInit :
        print str(count) + ': write: ' + d 
        serObj.write(d)
        dataWrote += d
        count += 1
    time.sleep(minDelay)
    return readStuff(serObj, count, len(dataWrote)/writeChunkSize)

def loopForEver(serObj,currentCount):
    # this does the infinite loop cycling the dataCycle elements
    while(True):
        for d in dataCycle:
            print str(currentCount) + ': write: ' + d
            serObj.write(d)
            time.sleep(max(minDelay,cycleDelay))
            count = readStuff(serObj, currentCount+1, len(d)/writeChunkSize) + 1
    
def main():
    # first see if a BT Device argument was provided
    port = smirfPort
    if len(sys.argv)>1 and (sys.argv[1] == "linvor"):
        port = linvorPort
    
    # now do the serial init
    ser = init(port)

    # then send any setup data to perpare for the cycling
    count = setup(ser) + 1
                
    # then loop
    loopForEver(ser,count)

if __name__ == '__main__':
    main()




