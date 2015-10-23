#temp3.py

# stack based ps2 bit reader
# almost works, 2015 09 28: 20:22, but loses track sometimes of where it is in the bit stream...


import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

DataPin = pyb.Pin('X1',pyb.Pin.IN,pull=pyb.Pin.PULL_NONE) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)


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

    bitsRead +=1
    inBuff[iIndex] |= DataPin.value() << rCount
    rCount +=1
    if (rCount==maxShift+1):
        rCount=0
        iIndex = (1+ iIndex) % bufferSize
        inBuff[iIndex]=0

def getValue(bits):
    return (bits>>1) & 255

def getter():
    global bufferSize, inBuff, iIndex, oIndex, rCount, maxShift

    if (iIndex != oIndex):
        res = getValue(inBuff[oIndex])
        oIndex = (1+ oIndex) % bufferSize
        return res
    else:
        return None
    
iFunc = reader

def interFunc(unused):
    global iFunc
    iFunc()

def setup():
    global ClockPin, DataPin 
    resetAll()
    
    release(ClockPin)
    release(DataPin)

    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, interFunc) 

    print('PS/2 tester. exit setup.')

def resetAll():
    global bufferSize, inBuff, iIndex, oIndex, rCount, maxShift,bitsRead
    inBuff     = [0 for i in range(bufferSize)]
    maxShift = 10
    iIndex = 0
    oIndex = 0
    rCount = 0
    bitsRead=0
    
def run():
    setup()
    valCounter=0
    triplet = [0,0,0]
    while(True):
        val = getter()
        if (None != val):
            if (bitsRead%11):
                resetAll()
                triplet=[0,0,0]
                valCounter=0
            else:
                triplet[valCounter]=val
                valCounter = (valCounter+1)%3
                if (valCounter == 0):
                    print('[%X, %X, %X]' % tuple(triplet))
                    print('Bits Read: %d' %bitsRead)
                    print('Bits Read mod 11:  %d'% (bitsRead%11))


bit=True        
def test():
    global bit, DataPin,inBuff
    
    if bit:
        DataPin.high()
    else:
        DataPin.low()
    reader()
    bit =  not bit
    print(inBuff)


def test2():
    global bit, DataPin,inBuff
    
    if bit:
        DataPin.high()
    else:
        DataPin.low()
    reader()
    bit =  not bit
    print(getter())

    
        
