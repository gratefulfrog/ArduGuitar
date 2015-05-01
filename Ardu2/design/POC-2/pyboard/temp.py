# temp.py
# this sends vectors of bits via spi incrementing by one at each send


import pyb 
from app import App
from state import State

"""
vLen = 13
bits= 256

s= spiMgr.SPIMgr(1,'X5')

def doit(v=3):
    vect = [0 for k in range(vLen)]
    for i in range (vLen):
        for j in range(bits):
            vect[i] = j
            s.update(vect)
            pyb.delay(v)

def lowBits(val=255,d=1):
    vect = [0 for k in range(vLen)]
    for i in range (vLen):
        vect[i] = val
        print (vect)
        s.update(vect)
        pyb.delay(d)
    
"""
def newLoad(obj,conf):
    obj.set('M',State.Vol,State.l0)
    obj.set('A',State.Vol,State.l0)
    obj.set('B',State.Vol,State.l0)
    obj.set('C',State.Vol,State.l0)
    obj.set('D',State.Vol,State.l0)
    obj.x()
    
    obj.loadConfig(conf)

def tremolo(obj,dely = 10):
    while True:
        obj.set('M',State.Vol,State.l0)
        obj.x()
        pyb.delay(dely)
        obj.set('M',State.Vol,State.l5)
        obj.x()
        pyb.delay(dely)

def vibrato(obj, dely=10):
    obj.set('M',State.ToneRange,State.l5)
    obj.x()
    while True:
        obj.set('M',State.Tone,State.l0)
        obj.x()
        pyb.delay(dely)
        obj.set('M',State.Tone,State.l4)
        obj.x()
        pyb.delay(dely)
