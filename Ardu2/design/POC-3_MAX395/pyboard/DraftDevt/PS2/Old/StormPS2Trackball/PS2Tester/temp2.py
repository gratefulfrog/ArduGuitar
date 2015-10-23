# temp2.py ps/2 testing

import pyb
import ps2BitReader
import micropython
micropython.alloc_emergency_exception_buf(100)

DataPin = pyb.Pin('X1',pyb.Pin.IN,pull=pyb.Pin.PULL_NONE) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

rIndex=0
oIndex=0
rCount=0
buffSize=5
readBuff = [ps2BitReader.ps2BitReader() for i in range(buffSize)]
outBuff=[0,0,0]
readCount=0

def hold(pin):
    pin.init(pyb.Pin.OUT_PP)
    pin.value(0)
    
def release(pin):
    pin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

# The ISR for the external interrupt in read mode
def ps2int_read():
    global DataPin, readBuff, rIndex, buffSize,readCount
    
    readBuff[rIndex].addBit(DataPin.value())
    if(readBuff[rIndex].isFull()):
        readCount+=1
        rIndex = (1 +rIndex) % buffSize
    
iFunc = ps2int_read

def interFunc(unused):
    global iFunc
    iFunc()

def setup():
    global ClockPin, DataPin 
    
    release(ClockPin)
    release(DataPin)

    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, interFunc) 

    print('PS/2 tester. exit setup.')

def loop():
    global outBuff,rCount,readBuff,oIndex,buffSize,readCount

    if (readCount):
        readCount -= 1
        outBuff[rCount]=readBuff[oIndex].getValue()
        oIndex = (oIndex + 1) % buffSize
        rCount += 1
        if (rCount==3):
            print ('[%X, %X, %X]' % tuple([i for i in buff]))
            outBuff = [0,0,0]
            rCount=0

            
def run():
    setup()
    while(True):
        loop()
