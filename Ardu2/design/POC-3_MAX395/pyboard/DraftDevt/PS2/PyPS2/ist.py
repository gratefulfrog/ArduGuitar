#ist.py
""" using 2 pins per funciton: a Control pin, and an input pin
wiring:
- input pin Pin.IN, PULL_NONE, is wired to external 1K pull up
- control pin PIN.OUT_OD, PULL_NONE, is wired to input pin
- interrupt is configured on input pin

IT WORKS!!!

""" 
import pyb
from pyb import Pin,ExtInt

"""
reset = [0xFF,3,0xFA,0xAA,0x0] # ACK, BAT, ID
remoteMode = [0xF0,1,0xFA] # ACK
poll = [0xEB,4,0xFA]  # ACK plus 3 data bits
"""

counter = 0
start = pyb.micros()

def simple(line):
    #print('Line:\t' +str(line))
    print('hello')

def count(line):
    global counter
    print(counter)
    counter +=1

def timeIt(line):
    global start
    print(pyb.elapsed_micros(start))
    start=pyb.micros()

ccb=0
cb = [simple,count,timeIt]

def callback(line):
    #print('ok')
    global cb,ccb
    cb[ccb](line) 
        
mdO = Pin.OUT_OD
mdI = Pin.IN
pL = Pin.PULL_NONE
iM = ExtInt.IRQ_FALLING
   
ci = Pin('X1',mdI,pL)
co = Pin('X2',mdO,pL)
di = Pin('X3',mdI,pL)
do = Pin('X4',mdO,pL)

def setInterrupt(p):
    ExtInt(p, iM, pL, callback)

def init():
    global ci
    setInterrupt(ci)

"""
def run(cbIndex):
    global ccb
    ccb=cbIndex
    if ccb==1:
        lastCount=0
        while True:
            if lastCount !=count:
                print(count)
                lastCount=count
    elif ccb==2:
        
"""
