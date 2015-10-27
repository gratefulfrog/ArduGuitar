#is0.py
""" using 2 pins per funciton: a Control pin, and an input pin
wiring:
- input pin Pin.IN, PULL_NONE, is wired to external 1K pull up
- control pin PIN.OUT_OD, PULL_NONE, is wired to input pin
- interrupt is configured on input pin

IT WORKS!!!

I have succeeded in writing out and reading in from circ buffers using the clock from the ps/2 beast!
period = 170 usecs

Now to try it with pins!
ok, period is 100 uSecs

Now try it with @micropython.native for reader and writer
ok, period still around 100 uSecs

what about viper?
can't get it to work...

what about not using a circBuff, just reading it straight into a buff

"""

import pyb
from pyb import Pin,ExtInt
from circBuff import circBuff

import micropython
micropython.alloc_emergency_exception_buf(100)


#############################
#  Pin Definitions
############################
mdO = Pin.OUT_OD
mdI = Pin.IN
pL = Pin.PULL_NONE
iM = ExtInt.IRQ_FALLING
   
ci = Pin('X1',mdI,pL) # clock input
co = Pin('X2',mdO,pL) # clock output (control pin)
di = Pin('X3',mdI,pL) # data input
do = Pin('X4',mdO,pL) # data output (control pint)

cv=co.value
dv=do.value
##############

# a pretend data out pin
pdo= Pin('X5',Pin.OUT_PP,pL) # pretend data output pin
pdi= Pin('X6',Pin.IN,pL)     # pretend data input pin
pdov = pdo.value
pdiv = pdi.value

bitsExpected = interruptCounter=start = outData = inData = tbInData = tbOutData = period = None

def init():
    cv(0)
    dv(0)
    setInterrupt(ci)

def stop():
    dv(1)
    cv(0)

@micropython.native
def reader():
    global bitsExpected,inData,interruptCounter,period,start
    if bitsExpected == inData.nbElts:
        # we're done
        stop()
    else:
        inData.put(pdiv())
    period[interruptCounter] = pyb.elapsed_micros(start)
    interruptCounter+=1
    start=pyb.micros()

@micropython.native
def writer():
    global handlerIndex,outData,interruptCounter,period,start
    if outData.nbElts:
        pdov(outData.get()%2)
    else:
        handlerIndex ^=1
    period[interruptCounter] = pyb.elapsed_micros(start)
    interruptCounter+=1
    start=pyb.micros()

    
def readerCirc():
    global bitsExpected,inData,tbOutData,interruptCounter,period,start
    if bitsExpected == inData.nbElts:
        # we're done
        stop()
    else:
        inData.put(tbOutData.get())
    period[interruptCounter] = pyb.elapsed_micros(start)
    interruptCounter+=1
    start=pyb.micros()
    
def writerCirc():
    global handlerIndex,outData,tbInData,interruptCounter,period,start
    if outData.nbElts:
        tbInData.put(outData.get())
    else:
        handlerIndex ^=1
    period[interruptCounter] = pyb.elapsed_micros(start)
    interruptCounter+=1
    start=pyb.micros()

    
handlerVec = (reader,writer)
handlerIndex = 1

def interruptHandler(line):
    handlerVec[handlerIndex]()

def setInterrupt(p):
    ExtInt(p, iM, pL, interruptHandler)

def run(bitsOut=11,bitsIn=44):
    """
    try some advanced tests of reading and writing
    """
    global outData,inData,tbInData,tbOutData,period,bitsExpected,interruptCounter,start

    interruptCounter=0
    
    bitsExpected = bitsIn
    
    # a place for the host to receive data from the trackball
    inData=circBuff(bitsIn+1)
    # a place for the host to keep data to send to the trackball
    outData=circBuff(bitsOut+1)

    # a place for the trackball to receive pretend data from the host
    tbInData=circBuff(bitsOut+1)
    # a place for the trackball to keep pretend data to send to the host
    tbOutData=circBuff(bitsIn+1)
    
    # bits for the host to send to the trackball
    [outData.put(i) for i in range(bitsOut)]
    # bits that the trackball will send to the host
    [tbOutData.put(i) for i in range(bitsIn)] # pretend data

    # a place to keep the timing measurements
    period=[None for i in range(bitsOut+bitsIn+5)]

    # set up for loop exit
    doneWriting=False
    doneReading=False

    # release the wild PS/2 beast and start the clock!
    dv(0)
    cv(1)
    start=pyb.micros()
    while True:
        doneWriting = not outData.nbElts
        doneReading = (inData.nbElts == bitsExpected)
        if doneWriting and doneReading:
            print('Done.')
            break
    

