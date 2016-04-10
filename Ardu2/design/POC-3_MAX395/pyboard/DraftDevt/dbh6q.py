#!/usr/local/bin/python3.4
# dbh6q.py debounce hardware with q 

"""
This is the working routine to manage 6 interrupts with hardware debouncing and queueing

How does it work?
Overview: (with some details not discussed)
* a circular q is impelemented as an array of ints.
* the callback enqueues index
* an endless loop checks processes the value popped from the Q
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
from array import array


# declare nb pins, and ids, lines
nbPins = 6
pinIdVec = ['X9','X10','Y3','Y4','Y5','Y6']
lineDict = { 6:0, 7:1 , 8:2, 9:3,12:4, 13:5}

# make a simple circular queue
qLen = 20
q = array('i',[0 for x in range(qLen)])
pptr = 0  # put pointer
gptr = 0  # get pointer
qNbObj=0  # object counter

# interrupt mechanics and debounce globals 
interCount=0
eVec = [None for i in range(nbPins)]

# just for simutating results
output = [None,None]
newStuff = False

def push(v):
    global q,pptr,qNbObj
    if qNbObj == qLen:
        print("Q Full! ignoring push!")
    else:
        q[pptr] = v
        pptr = pptr+1 % qLen
        qNbObj += 1

def pop():
    global gptr,qNbObj
    res = None
    if qNbObj:
        res = q[gptr]
        gptr = (gptr+1) % qLen
        qNbObj -=1
    return res

def proc(val):
    global interCount,output,newStuff
    if val != None:
        # this is where to put the call to a function that actually does something.
        output = [val,interCount]
        newStuff = True

def updateDisplay():
    if newStuff:
        print('Switch:',output[0],'\tInterrupt Count: ',output[1])
        newStuff = False
        
# define ISR
def callback(line):
    global interCount
    interCount +=1
    push(lineDict[line])

def init():
    global eVec
    for i in range(nbPins):
        eVec[i]=ExtInt(pinIdVec[i], ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)

def loop():
    try:
        while True:
            proc(pop())
            updateDisplay():
    except KeyboardInterrupt:
        print('Test ended!\nBye ...')


