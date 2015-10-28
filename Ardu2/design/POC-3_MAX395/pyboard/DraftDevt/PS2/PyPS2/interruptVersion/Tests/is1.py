#is1.py   WORKING CODE!!!
""" using 2 pins per funciton: a Control pin, and an input pin
wiring:
- input pin Pin.IN, PULL_NONE, is wired to external 1K pull up
- control pin PIN.OUT_OD, PULL_NONE, is wired to input pin
- interrupt is configured on input pin
- this is done for both clock and data lines

This module provides both low level and medium level functionality for 
the host side of the ps/2 mouse protocol.

Details of the protocol are available at:
http://computer-engineering.org/ps2protocol/
http://computer-engineering.org/ps2mouse/
 
This module provides:
- 4 pins: 
  - clock in, clock out, data in data out, named
  - ci, co,  di, do
  - default values are X1,X2,X3,X4 but these can be changed if needed

- Command structure framework:
  - a command is a list [nbBitsExpectedInResponse, 10 bits of the command], no start bit

- Defined host commands
  - reset, remote, poll command structures

- Usage:
1. Overview
The timing of the ps/2 protocol is critical and the pyboard is not really fast, that's why 
everything had to become global variables...

The way this works is that the host sends a command and the device replies.  
I have NOT IMPLEMENTED STREAMING MODE! 

The commands and replies are frames of 11 bits, low order first. 
The bits in a frame are:
 start bit: 0
 8 bits of data:
 odd parity bit,
 stop bit: 1

When freed, the device runs the clock. It looks for bits at HIGH clock.
A command is sent by setting to zero, or one, the dataOut pin while the clock is low. 
This bit is then clocked in by the device while the clock is HIGH.

After a full 11 bits, the device replies with a certain number of 11 bit frames, depending on the command.
The host can read the dataIn pin while the closk is LOW.

There is still some issue with the end of a communication sequence, but I do not understand what it is! This
sometimes causes the device to freeze, sigh... Sadly, I implemented a timeout, based on the expecte time
for the reply, such that:
- if there's too much time without a full communication cycle:
  - abort,
  - set the resetOnExit flag to true so that anyone calling can take care of the state

So what does all that mean to the user?

2. Detailed usage:
the user must initialize the module with a call to init()
Then, a reset command must be issued
Then, a remote command to tell the device to wait for polls instead of streaming data
Then, poll as often as the user wants. 
The response to any command is available as a list of bits in the order received in inData.

an example (these functions are at the end of the module)

i()
r()
m()
while True:
  process(p())  # process the data, ie the user needs to write the 'process' function
  delay(20) to give the processor some time to do stuff

 
Module structure
1. globals:
   pin names,
   command objects (lists)
   Pin objects,
   global variables:
   bitsExpected  # how many bits in the response to the current command
   outData # bits to send, not including start bit
   inData  # bits that were read in last full read
   bits2Send  # number of bits to send out
   outBitCount  # number of bits that have been sent out
   inBitCount   # number of bits read from the device
   moduleInit  # status of init, ie True if the interrupt object has been created.
   resetOnExit = False  # status of exit from 'run()' used in timeout mgt code
   handlerVec  # a 2-tuple of reader & writer functions triggered by the interrupt
   handlerIndex # index refers to hadlerVec, and is changed from read to write by the reader, 
                # initialized to writer since we always start by writing a command

2. init():
   This must be called first. It locks the clock and data to prevent the device from doing anything,
   then creates the interrupt object on LOW on the clock input pin. We are now ready to issue commands
3. stop() 
   the device is prevented from clocking. User should never need this.
4. reader()
   This is triggered by the Low clock interrupt. If we have read as much as expected, call stop()
   otherwise, clock in more data fro the data In pin and update the count
5. writer()
   as long as there are bits to send, clock them out; otherwise set the handlerIndex to the reader
   so that the next clock low will tirgger that
6. interruptHandler
   This is the callback exectued by the interrupt obect. It is simply an indirection on the handlerIndex.
7. setInterrupt
   creates the ExtInt interrupt obect
8. run(out,bitsInn,bitsOut)
   This is the workhorse of the module.
   It takes the arguments:
   - bits: the bits to send, low first, no start
   - bitsIn: the nb of bits that the reply should conatain
   - doTimeOut: boolean to indicate if we should set a timeout for response, needed in case of RESET 
                since it takes unspecified time.                
   then sets up the global envt. for the clocking out and in.
   the local 'done' flags are set False
   setup the envt for the time out!
   - by default, no reset on exit
   - compute the timeout needed, a 11 bit cycle takes areound 1100 uSecs, so we'll give it 1200 to be nice,
   - create a lambda closure for the test
   if not doing a time out: make a lambda <- True
 
   the hard coded ZERO start bit is set,
   the clock is released,
   as long as not done, just sit around waiting for interrupts
   when done, give it another init() to help prevent freezing!!!
9. c(tup,doTimeOut=False)
   sets up the call to run with tup[1],tup[0],doTimeOout
10. check(v)
    argument v is a string name of the command
    This function looks at the inData and determines if the response is ok, for the given command
    returns True if it is good, False if not
12. End User Functionality
12.1 r(prn=False)
     runs the RESET command. 
     Note: the reset can take a long time, so the timeout is disabled
     Prints the result of 'check' if arg is True.
     returns the tuples interpreted from the inData response
12.2 m(prn=False)
     runs the REMOTE command. 
     Prints the result of 'check' if arg is True.
     returns the tuples interpreted from the inData response
12.3 p(prn=False)
     runs the POLL command. 
     On return, check to see if resetOnExit is set:
     - run the RESET command,
     - return the tuple (None, None) to indicate that there was a problem
     Prints the result of 'check' and interpreted tuples if arg is True.
     returns the tuple (deltaX,delatY) as interpreted from the inData response,
     note: both deltaX and Y may overflow and in that case the value is None
12.3 i()
     runs init(). 
     This is just a convenience function.

IT WORKS,  I hope the hanging issue is fixed with the timeout!
"""

import pyb
from pyb import Pin,ExtInt
import interpreter

import micropython
micropython.alloc_emergency_exception_buf(100)

########################################
####      user modifiable variables  ###
########################################
clockIn  = 'X1'
clockOut = 'X2'
dataIn   = 'X3'
dataOut  = 'X4'
########################################


### commands on 10 bits! since start bit is hard coded
### responses on 11 bits, since strat bit is effectively read from the device byt the host

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
   
ci = Pin(clockIn,mdI,pL) # clock input
co = Pin(clockOut,mdO,pL) # clock output (control pin)
di = Pin(dataIn,mdI,pL) # data input
do = Pin(dataOut,mdO,pL) # data output (control pint)

# shortcuts for speed to read/write the pin values
cv=co.value
dv=do.value
##############

# global variables
bitsExpected = outData = inData  =  0x00
bits2Send = outBitCount = inBitCount = 0x00
moduleInit = False
resetOnExit = False  # for experimental timeout code

# test variables, to be removed from real code
# lastAction =  'x'
# lastTime   = 0

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
    #global bitsExpected,
    global inData,inBitCount

    # for tests
    #global lastAction  
    #lastAction = 'r'

    if bitsExpected == inBitCount:
        # we're done
        stop()
    else:        
        inData[inBitCount]=dv()
        inBitCount += 0x01
        #print('bitin')

@micropython.native
def writer():
    global handlerIndex,outBitCount
    # for tests
    #global lastAction  
    #lastAction = 'w'
    if outBitCount < bits2Send:
        dv(outData[outBitCount])
        outBitCount += + 0x01
        #print('bitout')
    else:
        # we're done, switch to reading!
        handlerIndex ^=1

handlerVec = (reader,writer)
handlerIndex = 1

def interruptHandler(line):
    handlerVec[handlerIndex]()

def setInterrupt(p):
    return ExtInt(p, iM, pL, interruptHandler)

def run(out,bitsIn,doTimeOut): #,bitsOut=10):
    """
    This is the workhorse of the module
    """
    global outData,inData,bitsExpected,bits2Send,outBitCount,inBitCount,handlerIndex

    ## experimental stuff
    global resetOnExit
    ### end experimental stuff
    
    inBitCount=outBitCount=0
    
    bitsExpected = bitsIn
    #bits2Send = bitsOut
    bits2Send = 10 # len(out)

    handlerIndex = 1
    
    # a place for the host to receive data from the trackball
    inData=[None for i in range(bitsExpected)]
    # a place for the host to keep data to send to the trackball and
    outData = [b for b in out]

    # set up for loop exit
    doneWriting=False
    doneReading=False

    # experimental stuff
    # implement a time out to return from function if timed out
    # time out value is (nb total bits/11) 1200uSecs, ie. the frame time is around 1100 us so give it
    # a tiny bit more
    resetOnExit=False
    timeOut = (11 + bitsIn) * 1200 /11
    start = pyb.micros()
    tFunc = lambda : pyb.elapsed_micros(start)>timeOut
    if not doTimeOut:
        tFunc = lambda : False
    #### end of experimental secion
    
    dv(0) # this is the start bit!
    cv(1)
    while True:
        doneWriting = (outBitCount == bits2Send) 
        doneReading = (inBitCount == bitsExpected)
        if doneWriting and doneReading:
            #print('Done.')
            break
        elif tFunc():
            #print('timed out...')
            pyb.delay(1)
            resetOnExit = True
            break

def c(tup,doTimeOut=True):
    run(tup[1],tup[0],doTimeOut)

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

###############################################
########## END USER FUNCTIONS Follow ##########
###############################################

def r(prn=False):
    """"
    send the RESET command and read response
    """
    c(reset,False)
    if prn:
        print(check('reset'))
    return [interpreter.deviceResponse(i) for i in interpreter.i11s(inData)]

def m(prn=False):
    """"
    send the REMOTE command and read response
    """
    c(remote)

    if prn:
        print(check('remote'))
    return [interpreter.deviceResponse(i) for i in interpreter.i11s(inData)]

def p(prn=False):
    """"
    send the POLL command and read response
    """
    c(poll)
    if resetOnExit:
        run(reset[1],reset[0],False)
        return (None,None)
    else:
        tups = interpreter.i11s(inData)
        if prn:
            print(check('poll'))
            print(interpreter.deviceResponse(tups[0]))
        return interpreter.interpretPollPayload(tups[1:])

# for deugging
def i():
    """
    initialize the module
    """
    init()

########################################
########################################
