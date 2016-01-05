#!/usr/local/bin/python3.4
# dbh6.ph debounce hardware 

"""
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

# itnerrupt mechanics and debounce globals 
flagVec= [False for i in range(nbPins)]
interCount=0
eVec = [None for i in range(nbPins)]
#loopDelay = 20

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
            #delay(loopDelay)
    except KeyboardInterrupt:
        print('Test ended!\nBye ...')


