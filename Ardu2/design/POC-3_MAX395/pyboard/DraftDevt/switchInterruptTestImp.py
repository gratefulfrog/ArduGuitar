#!/usr/local/bin/python3.4
# selectorInterruptTestImp.py
# exercise the switches with interrupts and no need for de bouncing

from switchInterruptTestImp import *

"""
Pyboard:
Switch pins: X19, X20, X21
led pins: X1, X2, X3 

usage:
>>> init()
>>> loop()

"""

from pyb import Pin,ExtInt,delay,millis,elapsed_millis

nbSwitches = 3

debounceDelay = 300 #millisecs 300 seems to be the minimum
loopDelay = 50 # millisecs 

# declare the pin ids
pinIds = ('X19','X20','X21') # interrupts 0,1,2

# define some leds instead of pickkups
ledPinNames= ('X1','X2','X3')
ledPins =[None,None,None] # will contain the switchg Pin objects when initialized
sPins =[None,None,None] # will contain the switchg Pin objects when initialized
eVec=[None,None,None] # will contain the extint objects when initialized

# itnerrupt mechanics and debounce 
flagVec= [False,False,False] # flags to be set by the interrupt callback
lastInterT = 0

switchPosNames=('left','middle','right')
interCount=0

# define ISR's
def callback(line):
    """
    The callback simply:
    - sets the corresponding flag,
    - prints a message
    """
    global interCount,eVec,flagVec
    flagVec[line] = True
    print(interCount,': Interrupt received: ',switchPosNames[line])
    interCount +=1

def init():
    """
    init the objects and vectors containing them
    set all Leds to off
    """
    global ledPins,sPins,eVec

    for i in range(nbSwitches):
        sPins[i] = Pin(pinIds[i],Pin.IN,Pin.PULL_UP)
        eVec[i]=ExtInt(sPins[i], ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)
        ledPins[i] = Pin(ledPinNames[i], Pin.OUT_PP)
        ledPins[i].low()


def doFlag (line):
    """
    This is called when a flag (line) is found to be True:
    - if there hasn't been enough time, reset flag and return
    - otherwise
    - toggle the corresponding led
    - reset the flag to false
    - print a message
    """
    global ledPins,flagVec,eVec,lastInterT

    # if not enough time, reset flag and return
    flagVec[line] = False
    if elapsed_millis(lastInterT) < debounceDelay: 
        return
    lastInterT = millis()
    ledPins[line].value(ledPins[line].value()^1)
    print('LED: ',line, 'toggled to:',ledPins[line].value(), '\ttime:', lastInterT)
        
def loop():
    """
    loop over all the flags and doFlag if true,
    clean exit if Ctrl-C detected
    """
    try:
        while True:
            [doFlag(i) for i in range(nbSwitches) if flagVec[i]]
            delay(loopDelay)
    except KeyboardInterrupt:
        print('Test ended!\nAll off ...')
        [ledPins[i].low() for i in range(nbSwitches)]

