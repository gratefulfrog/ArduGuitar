#is1.py   WORKING CODE!!!
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

what about not using a circBuff, just reading it straight into a buff?
let's make a new file for that! is1.py
now we'll clean out all the object code...
and we are down to 60 uSecs!

This is with no decorator
>>> import is1
>>> is1.init()
>>> is1.run()
Done.
>>> is1.period
[496, 64, 64, 64, 64, 65, 65, 65, 65, 64, 62, 52, 69, 
63, 63, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 63, 
63, 63, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 
63, 63, 63, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 63, 63, 63, 68]
>>> 

using: @micropython.native is slower!
>>> is1.period
[491, 67, 67, 67, 67, 68, 68, 68, 67, 67, 65, 57, 71, 
65, 65, 65, 65, 65, 65, 65, 66, 66, 65, 66, 65, 65, 
65, 65, 65, 65, 65, 65, 65, 65, 66, 66, 66, 66, 65, 
65, 65, 65, 65, 65, 65, 65, 78, 47, 66, 66, 66, 65, 65, 65, 65, 65, 73]

and bytecode?
>>> is1.period
[481, 64, 64, 64, 65, 65, 65, 65, 64, 64, 62, 52, 69, 
62, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 63, 63, 
62, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 75, 50, 
57, 63, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 63, 63, 63, 63, 63, 69]

using native:
>>> import is1
>>> is1.init()
>>> is1.run()
Done.
full time:      4998
time/op:        90.87273
>>> 

using none (tiny bit better!)
>>> import is1
>>> is1.init()
>>> is1.run()
Done.
full time:      4989
time/op:        90.7091
>>> 

more tests seem to indicate that the native is better?
sent: RESET,
received: 
[0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 
 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

which means these but reversed
r0 = [0, 1, 0, 1, 1, 1, 1, 1][::-1] = [1, 1, 1, 1, 1, 0, 1, 0] = 0xFA (ACK)
r1 = [0, 1, 0, 1, 0, 1, 0, 1][::-1] = [1, 0, 1, 0, 1, 0, 1, 0] = 0xAA (BAT)
r2 = [0, 0, 0, 0, 0, 0, 0, 0][::-1] = [0, 0, 0, 0, 0, 0, 0, 0] = 0x00 (ID)

It Worked!!!
What about Set Remote?
reply is ACK: [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1]
let's see!    [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1]
YES!!!
and
poll?
got this:
[0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,   ACK
 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 
 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 
 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1]
ie
0, 1, 0, 1, 1, 1, 1, 1
0, 0, 0, 1, 0, 1, 0, 0
1, 0, 1, 1, 0, 0, 0, 0
0, 1, 1, 1, 1, 1, 1, 1
reversed
1111 1010 = 0xFA (ACK)
0010 1000 = 0x28 (-Y)
0000 1101 = 0x0D (X=13)
1111 1110 = 0xFE (Y=-2)
0000 0001
+       1 
0000 0010 = 
YES!!!

old news: but reset, rest fails on second call with response
[0, 
0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 
0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 1]


Now all is ok!
and even better!

>>> import is1
>>> is1.i()
>>> is1.r()
True
['ACK', 'BAT', 'ID']
>>> is1.m()
True
['ACK']
>>> is1.p()
True
polling interpretation not yet done!
['ACK']

"""

import pyb
from pyb import Pin,ExtInt
import interpreter

import micropython
micropython.alloc_emergency_exception_buf(100)

### commands! on 10 bits!
### responses on 11 bits!

responseBits =  11
#0xFF
reset =  (3*responseBits,
          [1 for i in range(10)]) # reply is 3 x 11bits
#0xF0
remote = (1*responseBits,
          [0, 0, 0, 0,
           1, 1, 1, 1,
           1, 1])  # reply is 1 x 11bits
#EB
poll =   (4*responseBits,
          [1, 1, 0, 1,
           0, 1, 1, 1,
           1, 1])  # reply 4 x11


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

bitsExpected = interruptCounter=start = outData = inData = tbInData = tbOutData = period = 0x00
bits2Send= outBitCount=inBitCount=0x00
moduleInit = False

def init():
    global moduleInit
    cv(0)
    pyb.udelay(110)
    dv(0)
    if not moduleInit:
        moduleInit=True
        setInterrupt(ci)

def stop():
    cv(0)

@micropython.native
def reader():
    #start=pyb.micros()
    global bitsExpected,inData,inBitCount
    if bitsExpected == inBitCount:
        # we're done
        stop()
    else:        
        inData[inBitCount]=dv()
        inBitCount += 0x01

@micropython.native
def writer():
    global handlerIndex,outData,outBitCount,bits2Send
    if outBitCount < bits2Send:
        dv(outData[outBitCount])
        outBitCount += + 0x01
    else:
        # we're done, switch to reading!
        handlerIndex ^=1

handlerVec = (reader,writer)
handlerIndex = 1

def interruptHandler(line):
    handlerVec[handlerIndex]()

def setInterrupt(p):
    return ExtInt(p, iM, pL, interruptHandler)

def run(out,bitsIn=33,bitsOut=10):
    """
    try some advanced tests of reading and writing
    """
    global outData,inData,bitsExpected,bits2Send,outBitCount,inBitCount,handlerIndex  #period,interruptCounter,

    inBitCount=outBitCount=0
    
    bitsExpected = bitsIn
    bits2Send = bitsOut

    handlerIndex = 1
    
    # a place for the host to receive data from the trackball
    inData=[None for i in range(bitsExpected)]
    # a place for the host to keep data to send to the trackball and
    outData = [b for b in out]

    # set up for loop exit
    doneWriting=False
    doneReading=False

    # give it a kick and release the wild PS/2 beast! 
    init()
    dv(0) # this is the start bit!
    cv(1)
    while True:
        doneWriting = (outBitCount == bits2Send) 
        doneReading = (inBitCount == bitsExpected)
        if doneWriting and doneReading:
            #print('Done.')
            break
    # give it another kick, why?
    init()

def c(tup):
    run(tup[1],tup[0])

def check(v):
    d = {'reset':  [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 
                    0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
         'remote': [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
         'poll':   [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,   # note only check the ACK and the 8 bit always set!
                    0, 0, 0, 0, 1]}
    return all(map(lambda x,y:x==y,
                   inData,
                   d[v]))

def r(prn=False):
    c(reset)
    if prn:
        print(check('reset'))
    return [interpreter.deviceResponse(i) for i in interpreter.i11s(inData)]

def m(prn=False):
    c(remote)
    if prn:
        print(check('remote'))
    return [interpreter.deviceResponse(i) for i in interpreter.i11s(inData)]

def p(prn=False):
    c(poll)
    tups = interpreter.i11s(inData)
    if prn:
        print(check('poll'))
        print(interpreter.deviceResponse(tups[0]))
    return interpreter.interpretPollPayload(tups[1:])

# for deugging
def i():
    init()

