#!/usr/local/bin/python3.4
# selectorInterruptTest.py
# exercise the Seclector with interrupts

"""
Pyboard:
Selector pins: X19, X20, X21
led pins: X1, X2, X3 
"""

from pyb import Pin,ExtInt

# declare the pin ids
pinIds = ('X19','X20','X21') # interrupts 0,1,2

# define some leds instead of pickkups
ledPinNames= ('X1','X2','X3')
ledPins =[None,None,None]
sPins =[None,None,None]

switchPosNames=('left','middle','right')

interCount=0

# define ISR's
def callback(e):
    global interCount
    print(interCount,': Interrupt received: ',switchPosNames[e], 'pin value: ', sPins[e].value())
    #ledPins[e].value(sPins[e].value()^1)

def init():
    global ledPins,sPins,interCount
    interCount=0

    for i in range(3):
        sPins[i] = Pin(pinIds[i],Pin.IN,Pin.PULL_UP)
        ExtInt(sPins[i], ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, callback)
        #ledPins[i] = Pin(ledPinNames[i], Pin.OUT_PP)
        #ledPins[i].value(sPins[i].value()^1)
        



