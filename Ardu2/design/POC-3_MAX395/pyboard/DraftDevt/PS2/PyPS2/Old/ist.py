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
start = 0
sm=0
nb=0
avg=0
period=0
flag = False

mdO = Pin.OUT_OD
mdI = Pin.IN
pL = Pin.PULL_NONE
iM = ExtInt.IRQ_FALLING
   
ci = Pin('X1',mdI,pL)
co = Pin('X2',mdO,pL)
di = Pin('X3',mdI,pL)
do = Pin('X4',mdO,pL)

dv=do.value
bVec = [i for i in range(11)]
v=0

target=0
reading= False

def simple(line):
    global flag
    flag=True

def count(line):
    global counter
    counter +=1

def simpleTime(line):
    global start,period
    period = pyb.elapsed_micros(start)
    start=pyb.micros()
    
def timeIt(line):
    global start,sm,nb,avg
    sm = sm + pyb.elapsed_micros(start)    
    nb = nb + 1
    #print('timeIt')
    start=pyb.micros()

def likeReal(line):
    global v,period,target,start,reading
    target = bVec[v]
    v = (v+1)%11
    period = pyb.elapsed_micros(start)
    start=pyb.micros()

ccb=0
cb = [simple,count,timeIt,simpleTime,likeReal]

def callback(line):
    global cb,ccb
    cb[ccb](line) 
        
def setInterrupt(p):
    ExtInt(p, iM, pL, callback)

def simpleRunner():
    global flag,co
    co.value(1)
    flag=False
    while True:
        if flag:
            print('toc!')
        else:
            print('tic')
        flag=False

def countRunner():
    global co,counter
    counter=0
    co.value(1)
    while True:
        print('count:\t' +str(counter))

def timeItRunner():
    global start,co,avg,sm,nb
    sm=nb=0
    start=pyb.micros()
    co.value(1)
    while True:
        avg = 0 if not nb else sm/nb
        print('avg:\t' + str(avg))

def simpleTimeRunner():
    global co,period
    period=0
    co.value(1)
    while True:
        print('period:\t' +str(period))

def realRunner():
    global co,do,period,v
    period=v=0
    callCount=0
    do.value(0)
    co.value(1)
    passed=False
    while True:
        if passed and not v:
            print('end!')
            break
        print(str(callCount) +'\tperiod:\t' +str(period))
        callCount+=1
        passed =True
        
runVec = [simpleRunner,
          countRunner,
          timeItRunner,
          simpleTimeRunner,
          realRunner]

def rel(v):
    global ccb
    ccb=v
    runVec[v]()
    
def init():
    global ci,co
    co.value(0)
    do.value(0)
    setInterrupt(ci)

def stop():
    global co
    do.value(1)
    co.value(0)
