#!/usr/local/bin/python3.4
# dbh6.ph debounce hardware 

"""
This is the working routine to manage 6 interrupts with hardware debouncing.

How does it work?
Overview: (with some details not discussed)
* a vector flagVec contains ints, initially set to zero, for each pin.
* the callback increments the flagVec[pin]
* an endless loop checks the value of flagVec[each pin] and if >0, does the flag(pin).
* the doFlag(pin) is only called whe flagVec[pin]>0, we want to filter out any bouncing,
  so we only act on the first call, i.e. when flagVec[pin] == 1
  If it is so, we print out the info (this is where we would put a call to do something),
  we increment the global interrupt count.
  In all cases we reset flagVec[pin]
* the endless loop is enclosed in a try/except to allow for clean exit in case of keyboard interrupt.

Pyboard:
Switch pins, interrupt lines:
X9  :  06 
X10 :  07
Y3  :  08
Y4  :  09
Y5  :  12
Y6  :  13

usage:
>>> init()
>>> loop()
"""

#from pyb import ExtInt,Pin,delay
from pyb import ExtInt,Pin


# declare nb pins, and ids, lines
nbPins = 6
pinIdVec = ['X9','X10','Y3','Y4','Y5','Y6']
lineDict = { 6:0, 7:1 , 8:2, 9:3,12:4, 13:5}

# interrupt mechanics and debounce globals 
flagVec= [False for i in range(nbPins)]
interCount=0
eVec = [None for i in range(nbPins)]

# define ISR
def callback(line):
    global flagVec
    flagVec[lineDict[line]] += 1

def init():
    global eVec
    for i in range(nbPins):
        eVec[i]=ExtInt(pinIdVec[i], ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)

def doFlag (ind):
    global flagVec,interCount
    if flagVec[ind] ==1:
        # this is where to put the call to a function that actually does something.
        print('Switch:',ind, '\tFlag: ', flagVec[ind],'\tInterCount: ',interCount)
        interCount +=1
    flagVec[ind]=0
            
def loop():
    i = 0
    try:
        while True:
            if flagVec[i]>0:
                doFlag(i)
            i = (i+1) % nbPins
    except KeyboardInterrupt:
        print('Test ended!\nBye ...')


