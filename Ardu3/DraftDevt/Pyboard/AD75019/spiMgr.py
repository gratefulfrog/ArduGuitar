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
    def __init__(self,spiOnX,latchPin,prescaler=32,DEBUG=True):
        # create an SPI.MASTER instance on the 'X' side of the board, 
        # first arg=1 means 'X side' of the board

        if DEBUG:
            from _pyb import SPI,Pin,delay
        else:
            from pyb import SPI,Pin,delay

        boardSide = 1
        if not spiOnX:
            boardSide = 2
        self.spi = SPI(boardSide,SPI.MASTER,prescaler=prescaler,polarity=0)
        # create the pclk pin on the "latch" pin
        self.pclk = Pin(latchPin, Pin.OUT_PP)

    def update(self,byteArray):
        # set latch to high
        # send the data bits to the shift register
        # unset the latch
        self.pclk.high()
        # send the bits
        #print('send:\t' + byteArray)
        """
        for b in byteArray:
            print('send:\t{0:02x}x'.format(b))
        """
        self.spi.send(byteArray)
        self.pclk.low()
        # perhaps a small delay is needed here?? to cover the 65ns min pulse time.
        self.pclk.high()

    def __repr__(self):
        return 'SPIMgr:' + \
            '\n' + str(self.spi) + \
            '\nPCLK:\n' + str(self.pclk)

def connect(x,y,set,b):
    """ 
    set the value of the bit arr to zero or 1 depending on set argument
    to disconnect or connect the x,y pins
    note: this physically modifies the last argument bytearray b 
    """

    # first get the positon of the 2 x bytes:
    x15pos = (15-y)*2
    newBytes = bytearray([255,255])  # all set
    
    v= 1 << x
    v0 = (v>>8) & 255
    v1 = v & 255
    pair = (v0,v1)
    if set:
        for i in range(2):
            b[x15pos+i] |= pair[i]
    else:
        for i in range(2):
            newBytes[i] ^= pair[i]
            b[x15pos+i] &= newBytes[i]

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
    
def testC1(debug=0,dl=10):
    s = SPIMgr(True,'X5',DEBUG=debug)
    if debug:
        from _pyb import delay
    else:
        from pyb import delay

    for x in range(16):        
        for y in range(16):
            b=bytearray(32)
            xConnect(x,y,1,b,s,debug)
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
