#!/usr/local/bin/python3.4
# dbh.ph debounce hardware 

"""
Pyboard:
Switch pins: Y1 or X19

usage:
>>> init()
>>> loop()
"""

from pyb import ExtInt,Pin

# declare the pin id
pinId = 'X19' # interrupt 0 'Y1' # interrupt 6

# itnerrupt mechanics and debounce globals 
flag= False
interCount=0
eObj = None

# define ISR
def callback(line):
    global flag
    flag += 1

def init():
    global eObj
    eObj=ExtInt(pinId, ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)

def doFlag ():
    global flag,interCount
    print('Flag:',flag,'\tInterCount: ',interCount)
    flag=0
    interCount +=1
            
def loop():
    try:
        while True:
            if flag>0:
                doFlag()
    except KeyboardInterrupt:
        print('Test ended!\nBye ...')


