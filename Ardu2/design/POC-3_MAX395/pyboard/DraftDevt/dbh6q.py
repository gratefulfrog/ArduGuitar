#!/usr/local/bin/python3.4
# dbh6q.py debounce hardware with q 

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

def push(v):
    global q,pptr,qNbObj
    if qNbObj == qLen:
        print("Q Full! ignoring push!")
    else:
        q[pptr] = v
        pptr = pptr+1 % qLen
        qNbObj += 1

def pop():
    global q,gptr,qNbObj
    res = None
    if qNbObj:
        res = q[gptr]
        interCount +=1
        gptr = pptr+1 % qLen
        qNbObj -=1
    return res

def proc(val):
    global interCount
    if val:
        # this is where to put the call to a function that actually does something.
        ind = val // 10
        val = val % 10
        print('Switch:',ind, '\tValue: ', val,'\tInterrupt Count: ',interCount)

# define ISR
def callback(line):
    interCount +=1
    push(lineDict[line]*10 + 1)

def init():
    global eVec
    for i in range(nbPins):
        eVec[i]=ExtInt(pinIdVec[i], ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)

def loop():
    try:
        while True:
            proc(pop())
    except KeyboardInterrupt:
        print('Test ended!\nBye ...')


