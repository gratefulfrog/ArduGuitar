#!/usr/local/bin/python3.4
# pyb.py for Off-pyboard testing
# here we find pyboard simulation classes for Off-board testing

import time

def millis():
    return time.time()

def delay(dela):
    time.sleep(dela)
        
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
    IN = 'IN'
    PULL_DOWN = 'PULL_DOWN'
    

    def __init__(self, latch, mode=None, pull = None):
        self.latchPin = latch
        self.pinOut = mode
        self.puLL = pull
        self.val = 0

    def high(self):
        self.val = 1
        print(str(self) + '\n\tset: HIGH')

    def low(self):
        self.val = 0
        print (str(self) + '\n\tset: LOW')

    def value(self):
        return self.val

    def __repr__(self):
        return 'Pin:' + \
            '\n\tLatchPin:\t' + str(self.latchPin) + \
            '\n\tPinOut:\t' + str(self.pinOut) + \
            '\n\tValue:\t' + str(self.val) 

class pwmAble:
    def __inti__(self):
        self.perc = 0

    def pulse_width_percent(self,percent):
                self.perc = percent

    def __repr__(self):
        return 'pwmAble: ' +'\n\t' + str(self.perc)
    
class Timer:
    PWM  = 0
    def __init__(self,pp,freq):
        self.pin = pp
        self.freq = freq

    def channel (self,ch,kind,pin):
        r = pwmAble()
        return r

    def __repr__(self):
        return 'A Timer!'
