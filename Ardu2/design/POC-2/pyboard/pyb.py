#!/usr/local/bin/python3.4
# pyb.py for off-pyboard testing
# here we find pyboard simulation classes for off-board testing

class SPI():
    """simulation SPI class provides basic SPI simulation
    - definitions
    - instance creation
    - send operation
    - repr
    usage:
    >>> from pyb import SPI
    >>> s = SPI(1,SPI.MASTER)
    >>> print(s)
    SPI:
	BoardSide:	1
	MasterOrSlave:	Master
    >>> s.send(0)
    send:	0b0
    >>> s.send(1)
    send:	0b1
    >>> s.send(2)
    send:	0b10
    """
    MASTER = 'Master'
    SLAVE = 'Slave'

    def __init__(self,side,MasterOrSlave):
        self.side = side
        self.MoS = MasterOrSlave 

    def send(self,bits):
        print("Simulated: send:\t{0:#b}".format(bits))
        
    def __repr__(self):
        return 'SPI:' + \
            '\n\tBoardSide:\t' + str(self.side) + \
            '\n\tMasterOrSlave:\t' + str(self.MoS)

class Pin():
    """simulation Pin class provides basic pin simulation
    - definitions
    - instance creation
    - high() low()  operations
    - repr
    usage:
    >>> from pyb import Pin
    >>> p = Pin('X5',Pin.OUT_PP)
    >>> print(p)
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
    >>> p.high()
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
    >>> p.low()
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
    """
    OUT_PP = 'OUT_PP'

    def __init__(self, latch, po):
        self.latchPin = latch
        self.pinOut = po
        self.value = 0

    def high(self):
        self.value = 1
        print(str(self) + '\n\tset: HIGH')

    def low(self):
        self.value = 0
        print (str(self) + '\n\tset: LOW')

    def __repr__(self):
        return 'Pin:' + \
            '\n\tLatchPin:\t' + str(self.latchPin) + \
            '\n\tPinOut:\t' + str(self.pinOut) + \
            '\n\tValue:\t' + str(self.value) 
