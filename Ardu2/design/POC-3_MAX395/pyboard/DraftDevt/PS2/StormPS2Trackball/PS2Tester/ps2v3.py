#ps2v3.py

# stack based ps2 bit reader
# almost works, 2015 09 28: 20:22, but loses track sometimes of where it is in the bit stream...


import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

DataPin = pyb.Pin('X1',pyb.Pin.IN,pull=pyb.Pin.PULL_NONE) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

# globals used in reading
bufferSize = 2
inBuff     = [0 for i in range(bufferSize)]
maxShift = 10
iIndex = 0
oIndex = 0
rCount = 0
bitsRead=0


def hold(pin):
    pin.init(pyb.Pin.OUT_PP)
    pin.value(0)
    
def release(pin):
    pin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

# isr for reading
def reader():
    global bufferSize, inBuff, iIndex, oIndex, rCount, maxShift,bitsRead

    # inc the bit counter
    bitsRead +=1
    # or in the bit read
    inBuff[iIndex] |= DataPin.value() << rCount
    #increment the bit rank counter
    rCount +=1
    # if the bit rank has reached the end of the 11 bits
    if (rCount==maxShift+1):
        # reset the rank counter
        rCount=0
        # increment the index of the buffer to start reading in the next series of 11 bits
        iIndex = (1+ iIndex) % bufferSize
        # zero the now current incoming bit buffer
        inBuff[iIndex]=0

def getValue(bits):
    # take the 11 bits, shift one to the right then mask and return
    return (bits>>1) & 255

# this routine takes the values out of the incoming buffer
def getter():
    global bufferSize, inBuff, iIndex, oIndex, rCount, maxShift

    # if the current incoming index is different from the last output index
    if (iIndex != oIndex):
        # res is the 8 bit value, stripped of start, parity, stop bits
        res = getValue(inBuff[oIndex])
        #increment the out index
        oIndex = (1+ oIndex) % bufferSize
        # return the value
        return res
    else:
        # the current index is the same, so we are still reading in bits, do nothing
        return None

# this is a trick to be able to change ISR's on the fly    
iFunc = reader
# this is the ISR that the chip knows about
def interFunc(unused):
    global iFunc
    iFunc()

# call once on initialization
def setup():
    global ClockPin, DataPin 
    resetAll()
    # this assumes that the ps/2 device is already initialized and in streaming mode
    # set up for reading
    release(ClockPin)
    release(DataPin)

    # create the interrupt handler on the clock pin, falling
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, interFunc) 

    print('PS/2 tester. exit setup.')

# call this to reset in case of need??? when???
def resetAll():
    global bufferSize, inBuff, iIndex, oIndex, rCount, maxShift,bitsRead
    inBuff     = [0 for i in range(bufferSize)]
    maxShift = 10
    iIndex = 0
    oIndex = 0
    rCount = 0
    bitsRead=0

# top level call
def run():
    setup()
    # set up counters and outgoing buffer
    valCounter=0
    triplet = [0,0,0]
    # now loop forever
    while(True):
        # check the last val read
        val = getter()
        if it is not None, then it is a real value, process it
        if (None != val):
            # but if by bad luck we don't have a 11 bit read, then bail out!
            if (bitsRead%11):
                resetAll()
                triplet=[0,0,0]
                valCounter=0
            else:
                # so we read a multiple of 11 bits!
                # insert it in the outgoing buffer
                triplet[valCounter]=val
                # inc the buffer index 
                valCounter = (valCounter+1)%3
                # if we have read 3 into the buffer, show the world!
                if (valCounter == 0):
                    print('[%X, %X, %X]' % tuple(triplet))
                    print('Bits Read: %d' %bitsRead)
                    print('Bits Read mod 11:  %d'% (bitsRead%11))
