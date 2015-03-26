#!/usr/local/bin/python3.4
# spiMgr.py
# exercise some pyboard SPI with as many 74HC595 shift registers connected
# as needed:
# as of 2015 03 26 this module has been tested:
#  - off-board
#  - on-board, but with no shift Registers connected

"""
This is the wiring used:
pin   
Shift Reg 1
8  : GND
9  : Shift Reg 0, pin 14 (serial data out-> serial data in)
10 : 5v
11 : X6 SHCP 
12 : X5 STCP (latch)
13 : GND (Output Enable)
14 : X8  (Serial Data In - MOSI)
16 : 5v
Q0-Q7 : LEDs 8-15

Shift Reg 0
8  : GND
9  : not connected
10 : 5v
11 : X6 SHCP 
12 : X5 STCP (latch)
13 : GND (Output Enable)
14 : X8  (Serial Data In - MOSI)
16 : 5v
Q0-Q7 : LEDs 0-7
"""
from pyb import SPI,Pin

class SPIMgr():
    """
    This class provides an interface to the hardware level SPI object which
    it encapsulates as a member. 
    When creating an instance you must provide the pyboard side and 
    the latch pin's name, eg.
    >>> from spiMgr import SPIMgr
    >>> from state import State
    >>> s = SPIMgr(State.spiOnX,State.spiLatchPinName)
    >>> print(s)
    SPIMgr:
    SPI:
	BoardSide:	1
	MasterOrSlave:	Master
    STCP:
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
    ++
    The class only provides one method: update(bitArray).
    This method is called with an array of ints representing the 
    bits to be set to one via an SPI call. The process is
    1. set the latch pin LOW
    2. send the bits, int by int
    3. set the latch pin to high
    Note that when doing off-board tests, the 'send' message will 
    appear twice.
    usage:
    >>> s.update([0,1,2,4,8,16])
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
    Simulated: send:	0b0
    send:	0b0
    Simulated: send:	0b1
    send:	0b1
    Simulated: send:	0b10
    send:	0b10
    Simulated: send:	0b100
    send:	0b100
    Simulated: send:	0b1000
    send:	0b1000
    Simulated: send:	0b10000
    send:	0b10000
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
    """
    def __init__(self,spiOnX,latchPin):
        # create an SPI.MASTER instance on the 'X' side of the board, 
        # first arg=1 means 'X side' of the board
        boardSide = 1
        if not spiOnX:
            boardSide = 2
        self.spi = SPI(boardSide,SPI.MASTER)
        # create the stcp pin on the "latch" pin
        self.stcp = Pin(latchPin, Pin.OUT_PP)

    def update(self,bitArray):
        # send the data bits to the shift register
        # turn off the latch
        self.stcp.low()
        # send the bits
        for r in bitArray:
            self.spi.send(r)
            #### COMMENT NEXT LINE FOR Off-Board TESTS!
            print("send:\t{0:#b}".format(r))
        # turn on the latch
        self.stcp.high()

    def __repr__(self):
        return 'SPIMgr:' + \
            '\n' + str(self.spi) + \
            '\nSTCP:\n' + str(self.stcp)
