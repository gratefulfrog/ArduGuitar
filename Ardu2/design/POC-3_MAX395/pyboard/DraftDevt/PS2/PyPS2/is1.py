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

"""

import pyb
from pyb import Pin,ExtInt

import micropython
micropython.alloc_emergency_exception_buf(100)

### commands! on 10 bits!
#0xFF
reset =  (33,
          [1 for i in range(10)]) # reply is 3 x 11bits
#0xF0
remote = (11,
          [0, 0, 0, 0,
           1, 1, 1, 1,
           1, 1])  # reply is 1 x 11bits
#EB
poll =   (44,
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

def init():
    cv(0)
    dv(0)
    setInterrupt(ci)

def stop():
    dv(1)
    cv(0)

@micropython.native
def reader():
    #start=pyb.micros()
    global bitsExpected,inData,inBitCount # ,interruptCounter,period
    if bitsExpected == inBitCount:
        # we're done
        stop()
    else:
        #inData[inBitCount]=pdiv()
        inData[inBitCount]=dv()
        inBitCount += 0x01
        #interruptCounter = int(interruptCounter)+ 0x01
        #period[interruptCounter] = pyb.elapsed_micros(start)

@micropython.native
def writer():
    #start=pyb.micros()
    global handlerIndex,outData,outBitCount,bits2Send #,interruptCounter,period
    if outBitCount < bits2Send:
        #pdov(outData[outBitCount])
        dv(outData[outBitCount])
        outBitCount += + 0x01
    else:
        handlerIndex ^=1
    #interruptCounter = interruptCounter + 0x01
    #period[interruptCounter] = pyb.elapsed_micros(start)

handlerVec = (reader,writer)
handlerIndex = 1

def interruptHandler(line):
    handlerVec[handlerIndex]()

def setInterrupt(p):
    ExtInt(p, iM, pL, interruptHandler)

def run(out,bitsIn=33,bitsOut=10):
    """
    try some advanced tests of reading and writing
    """
    global outData,inData,bitsExpected,bits2Send,outBitCount,inBitCount,handlerIndex  #period,interruptCounter,

    inBitCount=outBitCount=0
    #interruptCounter=0
    
    bitsExpected = bitsIn
    bits2Send = bitsOut

    handlerIndex = 1
    
    # a place for the host to receive data from the trackball
    inData=[None for i in range(bitsExpected)]
    # a place for the host to keep data to send to the trackball and
    # bits for the host to send to the trackball
    #outData=  [i for i in range(bitsOut)]
    #outData = [0]
    #outData = [1 for i in range(bitsOut)]
    outData = [b for b in out]

    # a place to keep the timing measurements
    period=[None for i in range(bitsOut+bitsIn+2)]

    # set up for loop exit
    doneWriting=False
    doneReading=False

    # start the clock and release the wild PS/2 beast! 
    start=pyb.micros()
    cv(0)
    pyb.udelay(110)
    dv(0) # this is the start bit!
    cv(1)
    while True:
        doneWriting = (outBitCount == bits2Send) 
        doneReading = (inBitCount == bitsExpected)
        if doneWriting and doneReading:
            print('Done.')
            break
    fulltime = pyb.elapsed_micros(start)
    print('full time:\t' +repr(fulltime))
    print('time/op:\t' +repr(fulltime/(bits2Send+bitsExpected)))
    

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
"""
broken!
def interpret():
    l=len(inData)
    i=0
    messages=[]
    # get the 11 bit lists seperated out
    while (i<l):
        messages +=[inData[i:i+11]]
        i+=11
    # reverse them
    print('separated:\t' + repr(messages))
    res=map(lambda m:m[::-1],messages)
    print('reversed:\t' + repr([i for i in res]))
    # strip start and end bits
    res=map(lambda l: l[1:-1],res)
    print('stripped of s&s\t' + repr([i for i in res]))
    #check parity
    for msg in res:
        p=1
        for i in msg[1:]:
            p ^=i
        if p!=msg[0]:
            return False
    #if we got here, then parity is good for all them
    # strip the parity bit
    res = map(lambda l: l[1:],res)
    print('stripped of parity:\t' + repr([i for i in res]))
    # now we have bytes, most significant to the left
    # now make a list of decimal values
    sRes=[]
    for msg in res:
        i=7
        s=0
        for b in msg:
            s+=b<<i
            i-=1
        sRes+=[s]
    print('summs:\t' + repr(sRes))
    hRes = map(lambda x: hex(x),sRes)
    print('hexed:\t' + repr(hRes))
    return [i for i in hRes]
"""
