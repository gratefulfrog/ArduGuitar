#!/usr/local/bin/python3.4
# switchInterruptTest.py
# exercise Switches with interrupts

"""
Pyboard:
Switch pins: X19, X20, X21
led pins: X1, X2, X3 
"""

from pyb import Pin,ExtInt,millis,elapsed_millis

# declare the pin ids
pinIds = ('X19','X20','X21') # interrupts 0,1,2

# define some leds instead of pickkups
ledPinNames= ('X1','X2','X3')
ledPins =[None,None,None]
sPins =[None,None,None]

eVec=[None,None,None]

switchPosNames=('left','middle','right')

interCount=0
lastGoodInterrupt = 0
interruptDelay = 10


# define ISR's
def callback(line):
    """
    toggle the pin corresponding to the switch
    """
    eVec[line].disable()
    global interCount,lastGoodInterrupt
    if elapsed_millis(lastGoodInterrupt) < interruptDelay:
        print("poo!")
        eVec[line].enable()
        return
    if sPins[line].value():
        print('piii!')
        eVec[line].enable()
        return

    print(interCount,': Interrupt received: ',switchPosNames[line]) #, 'pin value: ', sPins[e].value())
    ledPins[0].value(ledPins[0].value()^1)
    interCount +=1
    lastGoodInterrupt=millis()
    eVec[line].enable()

def init():
    global ledPins,sPins,interCount,lastGoodInterrupt
    interCount=0
    lastGoodInterrupt=millis()

    for i in range(3):
        sPins[i] = Pin(pinIds[i],Pin.IN,Pin.PULL_UP)
        eVec[i]=ExtInt(sPins[i], ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, callback)
        ledPins[i] = Pin(ledPinNames[i], Pin.OUT_PP)
        ledPins[i].low() # value(sPins[i].value()^1)
    print('init complete!')
    



