# temp.py ps/2 testing

import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

# Device specific settings, configured for Arduino Uno
#CLOCK_PIN_INT = 1 # Pin 3 attached to INT1 in Uno

DataPin = pyb.Pin('X1',pyb.Pin.IN,pull=pyb.Pin.PULL_NONE) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
bitcount=0
incoming=0
prev_ms=0 
valRead=False
val=0
buff =[]
rIndex=0
oIndex=0
rCount=0
buffSize=16
readBuff = [0 for i in range(buffSize)]
lreadBuff= [0 for i in range(buffSize)]

def hold(pin):
    # make it ab output pin
    pin.init(pyb.Pin.OUT_PP)
    pin.value(0)
    
def release(pin):
    # make it an input pin
    #pin.init(pyb.Pin.OUT_PP)
    #pin.high()
    pin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

# The ISR for the external interrupt in read mode
def ps2int_read():
    global DataPin, readBuff, rIndex, buffSize
    
    #valRead=True
    readBuff[rIndex] = DataPin.value()
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
    global bitcount,incoming,prev_ms,valRead,buff,rCount,readBuff,lreadBuff,rIndex,oIndex,buffSize

    if (oIndex != rIndex):
        now_ms = pyb.millis()
        if (now_ms - prev_ms > 250):
            bitcount = incoming = 0
            buff=[]
            oIndex=rIndex=rCount=0
            print('\tIn: (now_ms - prev_ms > 250)')
        prev_ms = now_ms
        if (bitcount <= 7):
            incoming |= (readBuff[oIndex] << bitcount)
            oIndex = (1+oIndex) % buffSize
        if (bitcount ==7 ):
            #print('\tIn: (bitcount == 7)')
            #print ('incoming= %d'%incoming)
            buff = buff+[incoming]
            rCount+=1
            if (rCount==3):
                print('buff: ',str(buff))
                rCount=0
                buff=[]
            bitcount=0
            incoming=0
        else:
            bitcount+=1
    if (readBuff!=lreadBuff):
        print('rIndex: ',str(rIndex),'  oIndex: ', str(oIndex))
        print('readBuff= ', str(readBuff))
        for i in range(len(lreadBuff)):
            lreadBuff[i]=readBuff[i]

def run():
    setup()
    while(True):
        loop()
