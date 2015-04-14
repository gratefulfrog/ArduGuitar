# temp.py
# this sends vectors of bits via spi incrementing by one at each send


import pyb 
import spiMgr

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
    
