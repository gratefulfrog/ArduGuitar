#!/usr/local/bin/python3.4
# spiMgr.py
# exercise some pyboard SPI with AD75019

"""
The pyboard SPI class gives details:
http://docs.micropython.org/en/latest/library/pyb.SPI.html

the NSS pin is NOT used by the SPI driver and is free for other use.

SPI(1) is on the X position: 
(NSS, SCK, MISO, MOSI) = (X5, X6, X7, X8) = (PA4, PA5, PA6, PA7)

SPI(2) is on the Y position: 
(NSS, SCK, MISO, MOSI) = (Y5, Y6, Y7, Y8) = (PB12, PB13, PB14, PB15)

This is the wiring used on the AD75019
pin   
4   Vss  -12v
3   SIN   Pyboard SPI MOSI
2   SCLK  Pyboard SPI CLK
1   PCLK  Pyboard X5
44  SOUT  NC
43  DGND  Pyboard GND
42  Vcc   +5v
41  Vdd   +12v

The clck frequency range for the chip is 20 kHz to 5 MHz.

SPI prescaler values that will work are therefore:
prescaler     baudrate
32            2 625 000  i.e. 2.625 MHz
256           328 125    i.e.   328 kHz
"""
import time

class SPIMgr():
    """
    This class provides an interface to the hardware level SPI object which
    it encapsulates as a member. 
    When creating an instance you must provide the pyboard side and 
    the latch pin's name, eg. 'X5'
    ++++++++++++++++++++++
    The class only provides one method: update(byteArray).
    This method is called with an bytearray (python built-in type!!) representing the 
    bits to be set to one via an SPI call. The process is
    1. set the latch pin HIGH
    2. send the bits with SPI send method
    3. set the latch pin to LOW pulse width min 65 ns
    4. set the latch pin to HIGH
    >>> import spiMgr
    >>> s =spiMgr.SPIMgr(True,'X5')
    >>> s
    SPIMgr:
    SPI:
	BoardSide:	1
	MasterOrSlave:	Master
	prescaler:	32
    PCLK:
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
    >>> s.update(bytearray([1,2,4,255])) 
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
    send:	bytearray(b'\x01\x02\x04\xff')
    Simulated: send:	0b1
    Simulated: send:	0b10
    Simulated: send:	0b100
    Simulated: send:	0b11111111
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH

    """
    def __init__(self,spiOnX,latchPin,prescalerR=32,DEBUG=False):
        # create an SPI.MASTER instance on the 'X' side of the board, 
        # first arg=1 means 'X side' of the board

        if DEBUG:
            from _pyb import SPI,Pin
        else:
            from pyb import SPI,Pin

        boardSide = 1
        if not spiOnX:
            boardSide = 2
        self.spi = SPI(boardSide,SPI.MASTER,prescaler=prescalerR,polarity=0,phase=0,firstbit=SPI.MSB)
        # create the pclk pin on the "latch" pin
        self.pclk = Pin(latchPin, Pin.OUT_PP)
        self.pclk.high()
        self.bitVec =  bytearray(32)

    def update(self,twice=False):
        # set latch to high
        # send the data bits to the shift register
        # unset the latch
        self.pclk.high()
        
        #print(''.join('{:02x}'.format(x) for x in self.bitVec))
        if twice:
            self.spi.send(self.bitVec+self.bitVec)
        else:
            self.spi.send(self.bitVec)    
        self.pclk.low()
        #time.sleep_us(1)
        # perhaps a small delay is needed here?? to cover the 65ns min pulse time.
        self.pclk.high()

    def connect(self, x,y,set):
        """ 
        set the value of the bit arr to zero or 1 depending on set argument
        to disconnect or connect the x,y pins
        note: this physically modifies the last argument bytearray b 
        """

        # first get the positon of the 2 x bytes
        x15pos = (15-y)*2
        # then set the correct bit for the x bit
        v    = 1 << x
        # pair contains a bit corresponding to the x pin
        pair = (((v>>8) & 255), (v & 255))
    
        for i in range(2):
            if set:
                # to set we just or the x bit
                self.bitVec[x15pos+i] |= pair[i]
            else:
                # to unset we and all the bits except the x bit
                self.bitVec[x15pos+i] &= (255 ^ pair[i])

    def clear(self):
        self.setAll(0)

    def setAll(self,v=255):
        for i in range(32):
            self.bitVec[i]=v

    def __repr__(self):
        return 'SPIMgr:' + \
            '\n' + str(self.spi) + \
            '\nPCLK:\n' + str(self.pclk) +\
            '\nbitVe:\n' + str(self.bitVec)
            

def waitSecs(n,debug=False):
   s = "wait " + str(n) + " seconds..."
   print(s)
   if debug:
          time.sleep(n)
   else:
       time.sleep_ms(int(1000*n))


def allOff(spi):
    print("turn everything off")
    spi.clear()
    spi.update()

def allOn(spi):
    print("turn everything on")
    spi.setAll()
    spi.update()

def connect00(spi,set):
    s = "Connecting 0,0: " + str(set)
    print(s)
    spi.connect(0,0,set)
    spi.update()

def test(y,expectedVal):
    return y.value() == expectedVal
    
def conTest(twice=False,debug=False):
    if debug:
        from _pyb import SPI,Pin
    else:
        from pyb import SPI,Pin


    # initiallize the pins for reading
    inputPinNameVec = ['Y1','Y2','Y3','Y4',
                       'Y5','Y6','Y7','Y8',
                       'Y9','Y10','Y11','Y12',
                       'X1','X2','X3','X4']
    inputPinVec =[]
    for pn in inputPinNameVec:
        inputPinVec.append(Pin(pn,Pin.IN,Pin.PULL_DOWN))
    
    # create the spiMgr instance
    print('creating the spiMgr and clearing all connections...')
    s=SPIMgr(True,'X5',DEBUG=debug)
    s.clear()
    s.update(twice)
    alreadyTested = []
    # now run the big matrix connection loop
    for x in range(16):
        for y in range(16):
            # first connect everyone who already passed
            print('reconnecting previously connected pins...')
            for (i,j) in alreadyTested:
                s.connect(i,j,True)
            # then make the unitary connection and test for connectivity
            print('connecting new pins: (',x,y,')')
            s.connect(x,y,True)
            s.update(twice)
            if twice:
                pass
                #waitSecs(5,debug)
            elif False:
                if not test(inputPinVec[y],1):
                    print(x,y, 'connection failed!')
                    print('Already Tested : ', alreadyTested)
                    for (i,j) in alreadyTested:
                        print('y:',j,'value :', inputPinVec[j].value())
                    raise ValueError
            # add the current pair to  alreadyTested
            alreadyTested.append((x,y))
            # then clear all and test all for for disconnectivity
            print('disconnecting all pins...')
            s.clear()
            s.update(twice)
            if twice:
                pass
                 #waitSecs(5,debug)
            elif False:
                for (i,j) in alreadyTested:
                    if not test(inputPinVec[j],0):
                        print(i,j, 'Disconnection failed!')
                        print('already Tested : ', alreadyTested)
                        for (i,j) in alreadyTested:
                            print('y:',j,'value :', inputPinVec[j].value())
                        raise ValueError
                
    print('Test Completed!')


    
def outTest(delay=5,debug=False):
    if debug:
        from _pyb import SPI,Pin
    else:
        from pyb import SPI,Pin


    # initiallize the pins for reading
    inputPinNameVec = ['Y1','Y2','Y3','Y4',
                       'Y5','Y6','Y7','Y8',
                       'Y9','Y10','Y11','Y12',
                       'X1','X2','X3','X4']
    inputPinVec =[]
    for pn in inputPinNameVec:
        inputPinVec.append(Pin(pn,Pin.IN,Pin.PULL_DOWN))
    
    # create the spiMgr instance
    print('creating the spiMgr and clearing all connections...')
    s=SPIMgr(True,'X5',DEBUG=debug)
    
    s.clear()
    s.update(True)
    while True:    
        # now run the big matrix connection loop
        for x in range(16):
            for y in range(16):
                # then make the unitary connection and test for connectivity
                print('connecting new pins: (',y,x,')')
                s.connect(y,x,True)
                s.update(True)
                waitSecs(delay,debug)
                s.connect(y,x,False)
    print('Test Completed!')


    
def runLoop(showTime=5):
    s=SPIMgr(True,'X5')

    while True:
        # flash 1x, turn everything off and wait showTime seconds
        print("\nStep: 1")
        #flash(1)
        allOff(s)
        waitSecs(showTime)

        # flash 2x, turn on (0,0)  wait showTime seconds,
        print("\nStep: 2")
        #flash(2)
        connect00(s,True)  
        waitSecs(showTime)
        
        # flash 3x, turn off (0,0) wait showTime seconds,
        print("\nStep: 3")
        #flash(3)
        connect00(s,False)
        waitSecs(showTime)
        
        # flash 4x, turn all on,   wait showTime seconds,
        print("\nStep: 4")
        #flash(4)
        allOn(s)
        waitSecs(showTime)
        
        # flash 5x, turn all off,  wait showTime seconds,
        print("\nStep: 5")
        #flash(5)
        allOff(s)
        waitSecs(showTime)
        
        # flash 6x, turn on (0,0), wait showTime seconds,
        print("\nStep: 6")
        #flash(6)
        connect00(s,True)
        waitSecs(showTime)
        
        # flash 7x, turn all off,  wait showTime seconds.
        print("\nStep: 7")
        #flash(7)
        allOff(s)
        waitSecs(showTime)
        
        print("\nDone")

def rangeConnect(spi,xLim,yLim,set=True):
    xRange = range(xLim+1)
    yRange = range(yLim+1)
    for x in xRange:
        for y in yRange:
            spi.connect(x,y,set)
    spi.update()

inputPinVec =[]

def initPins(debug=False):
    global inputPinVec
    if debug:
        from _pyb import SPI,Pin
    else:
        from pyb import SPI,Pin
    
    # init Y pins for reading from AD75019
    # this vec contains the pyboard pin names corresponding to y0, y1, y2...
    inputPinNameVec = ['Y1','Y2','Y3','Y4',
                       'Y5','Y6','Y7','Y8',
                       'Y9','Y10','Y11','Y12',
                       'X1','X2','X3','X4']
    # set up for input
    for pn in inputPinNameVec:
        inputPinVec.append(Pin(pn,Pin.IN,Pin.PULL_DOWN)) # pull down is only for testing...

def showRange(yLim):
    for y in range(yLim+1):
        print('Y: '+ "{:2d}".format(y) + ' = ' + str(inputPinVec[y].value()))


"""

def testSPI(debug=0,dl=100):
    s = SPIMgr(True,'X5',DEBUG=debug)
    if debug:
        from _pyb import delay
    else:
        from pyb import delay
    while(True):
        b = bytearray(32)
        for i in range(32):
            for j in range(256):
                b[i] = j
                s.update(b)
                delay(dl)

def showBits(b):
    for i in range(0,len(b),2):
        print('{0:08b}\t{1:08b}'.format(b[i],b[i+1]))

def showBitsL(b):
    s=''
    for i in b:
        s+='{0:08b}'.format(i)
    print(s)

def xConnect(x,y,c,b,s,debug=0):
    connect(x,y,c,b)
    if debug:
        showBitsL(b)
    else:
        s.update(b)
    
def testC1(c,debug=0,dl=10):
    s = SPIMgr(True,'X5',DEBUG=debug)
    if debug:
        from _pyb import delay
    else:
        from pyb import delay
    b=bytearray(32)
    for x in range(16):        
        for y in range(16):
            xConnect(x,y,c,b,s,debug)
            delay(dl)
                
def testCA(debug=0,dl=10):
    s = SPIMgr(True,'X5',DEBUG=debug)
    if debug:
        from _pyb import delay
    else:
        from pyb import delay

    b=bytearray(32)
    for x in range(16):        
        for y in range(16):
            xConnect(x,y,1,b,s,debug)
            delay(dl)
    delay(dl*10)
    for x in range(16):        
        for y in range(16):
            xConnect(x,y,0,b,s,debug)
            delay(dl)
    delay(dl*10)

def runCA(debug=0,dl=100):
    while 1:
        testCA(debug,dl)

def runUp(dl=50):
    s=SPIMgr(True,'X5')
    b= bytearray(32)
    c= bytearray(32)
    for i in range(15):
        for j in range(16):
            connect(i,j,1,b)
            print(i,j,'on')
            s.update(b)
            time.sleep_ms(dl)
            print('all off')
            s.update(c)
            time.sleep_ms(dl)

from spiMgr import *
s=SPIMgr(True,'X5') 

#s=SPIMgr(True,'X5',prescalerR=128)
#s=SPIMgr(True,'X5',prescalerR=256)
#s=SPIMgr(True,'X5',prescalerR=32)

#s=SPIMgr(True,'X5',prescalerR=64)

b=bytearray(32)
d=bytearray(32)
connect(0,0,1,d)
c = bytearray([255 for i in range(32)])
s.update(b)
s.update(d)
s.update(c)

#if 6 bytes are 0, i.e. 26 bytes are 255, then it requires 2x updating to 0 to get it all zeroed!

There is strange behavior.... This needs to be further tested and fixed!

"""
